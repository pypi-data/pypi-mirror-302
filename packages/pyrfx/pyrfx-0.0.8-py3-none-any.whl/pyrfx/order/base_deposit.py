import logging
from abc import ABC, abstractmethod
from logging import Logger
from typing import Any

from eth_account.datastructures import SignedTransaction
from hexbytes import HexBytes
from web3.contract import Contract
from web3.types import BlockData, ChecksumAddress, ContractFunction, TxParams

from pyrfx.approve_token import check_if_approved
from pyrfx.config_manager import ConfigManager
from pyrfx.gas_utils import get_execution_fee
from pyrfx.get.markets import Markets
from pyrfx.get.oracle_prices import OraclePrices
from pyrfx.utils import determine_swap_route, get_estimated_deposit_amount_out, get_exchange_router_contract


class Deposit(ABC):
    """
    A class to handle the creation and management of deposit orders in a decentralized exchange.

    This class is responsible for preparing deposit transactions, including setting up token paths,
    handling approvals, and submitting the final deposit transaction to the blockchain.
    It supports handling long and short token deposits, gas fee estimation, and token approvals.
    """

    @abstractmethod
    def __init__(
        self,
        config: ConfigManager,
        market_key: str,
        initial_long_token: str,
        initial_short_token: str,
        long_token_amount: int,
        short_token_amount: int,
        max_fee_per_gas: int | None = None,
        debug_mode: bool = False,
        log_level: int = logging.INFO,
    ) -> None:
        """
        Initialize the Deposit class with necessary configurations and contract objects.

        The constructor sets up various internal attributes based on the provided parameters, including
        initializing connections to blockchain contracts and retrieving market information. If `max_fee_per_gas`
        is not provided, it will be calculated based on the base fee of the latest block with a 35% multiplier.

        :param config: Configuration object containing blockchain network and contract settings.
        :param market_key: The unique key representing the market where the deposit will be made.
        :param initial_long_token: The address of the token to be deposited on the long side.
        :param initial_short_token: The address of the token to be deposited on the short side.
        :param long_token_amount: The amount of long tokens to be deposited in the market.
        :param short_token_amount: The amount of short tokens to be deposited in the market.
        :param max_fee_per_gas: Optional maximum gas fee to pay per gas unit. If not provided, calculated dynamically.
        :param debug_mode: Boolean indicating whether to run in debug mode (does not submit actual transactions).
        :param log_level: Logging level for this class.
        """
        self.config: ConfigManager = config
        self.market_key: str = market_key
        self.initial_long_token: str = initial_long_token
        self.initial_short_token: str = initial_short_token
        self.long_token_amount: int = long_token_amount
        self.short_token_amount: int = short_token_amount
        self.max_fee_per_gas: int = max_fee_per_gas or self._get_max_fee_per_gas()
        self.debug_mode: bool = debug_mode

        # Setup logger
        self.logger: Logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(log_level)

        self.long_token_swap_path: list = []
        self.short_token_swap_path: list = []

        self._gas_limits: dict = {}
        self._gas_limits_order_type_contract_function: ContractFunction | None = None

        # Internal setup of the blockchain connection and contracts
        self._exchange_router_contract_obj: Contract | None = get_exchange_router_contract(config)
        self.all_markets_info: dict[str, dict[str, Any]] = Markets(self.config).get_available_markets()

    @abstractmethod
    def determine_gas_limits(self) -> None:
        """
        Abstract method to determine gas limits for the deposit order.

        This method must be implemented by subclasses to handle the retrieval of
        gas limits specific to the operation being performed.
        """
        raise NotImplementedError("This method must be implemented by subclasses.")

    def check_for_approval(self) -> None:
        """
        Check if the long and short tokens are approved for spending. If not, approve them.

        :raises ValueError: If token approval fails.
        """
        spender: ChecksumAddress = self.config.contracts.router.contract_address

        tokens_to_check: list[tuple[str, int]] = [
            (self.initial_long_token, self.long_token_amount),
            (self.initial_short_token, self.short_token_amount),
        ]

        tokens_to_approve: list[tuple[str, int]] = [(token, amount) for token, amount in tokens_to_check if amount > 0]

        if not tokens_to_approve:
            self.logger.info("No tokens need approval.")
            return

        for token_address, amount in tokens_to_approve:
            try:
                self._approve_token_if_needed(token_address=token_address, amount=amount, spender=spender)
            except Exception as e:
                self.logger.error(f"Approval for token spending failed for {token_address}: {e}")
                raise ValueError(f"Approval for token spending failed for {token_address}: {e}")

    def _approve_token_if_needed(self, token_address: str, amount: int, spender: ChecksumAddress) -> None:
        """
        Helper method to check and approve a token if needed.

        :param token_address: The address of the token to be approved.
        :param amount: The amount of the token to approve.
        :param spender: The address of the spender.
        """
        if amount <= 0:
            return

        check_if_approved(
            config=self.config,
            spender_address=spender,
            token_to_approve_address=token_address,
            amount_of_tokens_to_approve_to_spend=amount,
            max_fee_per_gas=self.max_fee_per_gas,
            approve=True,
            logger=self.logger,
        )

    def create_and_execute(self) -> None:
        """
        Create a deposit order by estimating fees, setting up paths, and submitting the transaction.
        """
        try:
            # Check for token approvals unless in debug mode
            if not self.debug_mode:
                self.check_for_approval()

            # Setup addresses and estimate fees
            eth_zero_address: ChecksumAddress = self.config.zero_address
            ui_ref_address: ChecksumAddress = self.config.zero_address

            min_market_tokens: int = self._estimate_deposit()
            execution_fee: int = self._calculate_execution_fee()

            # Validate initial tokens and determine swap paths
            self._check_initial_tokens()
            self._determine_swap_paths()

            # Build transaction arguments once and pass to the multicall method
            arguments: tuple = self._build_transaction_arguments(
                user_wallet_address=self.config.user_wallet_address,
                eth_zero_address=self.config.zero_address,
                ui_ref_address=self.config.zero_address,
                min_market_tokens=min_market_tokens,
                execution_fee=execution_fee,
            )

            # Prepare the multicall arguments and calculate WNT amount
            multicall_args, total_wnt_amount = self._prepare_multicall_and_wnt_amount(
                arguments=arguments, execution_fee=execution_fee
            )

            # Submit the final transaction
            self._submit_transaction(
                user_wallet_address=self.config.user_wallet_address,
                value_amount=total_wnt_amount,
                multicall_args=multicall_args,
                gas_limits=self._gas_limits,
            )

        except Exception as e:
            self.logger.error(f"Failed to create deposit order: {e}")
            raise

    def _calculate_execution_fee(self) -> int:
        """Estimate and return the execution fee."""
        return int(
            get_execution_fee(
                gas_limits=self._gas_limits,
                estimated_gas_limit_contract_function=self._gas_limits_order_type_contract_function,
                gas_price=self.config.connection.eth.gas_price,
            )
            * 1.1
        )

    def _build_transaction_arguments(
        self,
        user_wallet_address: ChecksumAddress,
        eth_zero_address: ChecksumAddress,
        ui_ref_address: ChecksumAddress,
        min_market_tokens: int,
        execution_fee: int,
    ) -> tuple:
        """
        Construct the main transaction arguments for deposit order creation.

        :param user_wallet_address:
        :param eth_zero_address:
        :param ui_ref_address:
        :param min_market_tokens:
        :param execution_fee:
        :return:
        """
        return (
            user_wallet_address,
            eth_zero_address,
            ui_ref_address,
            self.market_key,
            self.initial_long_token,
            self.initial_short_token,
            self.long_token_swap_path,
            self.short_token_swap_path,
            min_market_tokens,
            True,  # should_unwrap_native_token
            execution_fee,
            0,  # callback_gas_limit
        )

    def _prepare_multicall_and_wnt_amount(self, arguments: tuple, execution_fee: int) -> tuple[list[HexBytes], int]:
        """
        Prepare the multicall arguments by handling long and short token amounts and adding the necessary WNT amount.

        :param arguments:
        :param execution_fee:
        :return:
        """
        multicall_args: list = []
        total_wnt_amount: int = sum(
            self._add_token_multicall(token_address=token, token_amount=amount, multicall_args=multicall_args)
            for token, amount in [
                (self.initial_long_token, self.long_token_amount),
                (self.initial_short_token, self.short_token_amount),
            ]
            if amount > 0
        )

        # Add WNT amount and deposit parameters to multicall
        multicall_args.extend(
            [
                HexBytes(self._send_wnt(amount=total_wnt_amount + execution_fee)),
                HexBytes(self._create_order(arguments=arguments)),
            ]
        )

        return multicall_args, total_wnt_amount

    def _add_token_multicall(self, token_address: str, token_amount: int, multicall_args: list) -> int:
        """
        Add token transfer to multicall and return WNT amount if necessary.

        :param token_address: Token address.
        :param token_amount: Token amount.
        :param multicall_args: Multicall arguments.
        :return: Token multicall amount.
        """
        if token_amount > 0:
            if token_address == self.config.weth_address:
                return token_amount
            multicall_args.append(HexBytes(self._send_tokens(token_address, token_amount)))
        return 0

    def _get_max_fee_per_gas(self) -> int:
        """
        Retrieve the latest block base fee and calculate the max fee per gas with a multiplier.

        :return: Max fee per gas.
        """
        return int(self.config.connection.eth.get_block("latest")["baseFeePerGas"] * 1.35)

    def _submit_transaction(
        self, user_wallet_address: str, value_amount: float, multicall_args: list, gas_limits: dict
    ) -> None:
        """
        Submit the deposit transaction to the blockchain.

        :param user_wallet_address: The address of the user's wallet.
        :param value_amount: The amount of ETH (or equivalent) to send with the transaction.
        :param multicall_args: A list of encoded contract function calls.
        :param gas_limits: Gas limit details for the transaction.
        :return: None.
        """
        self.logger.info("Building transaction ...")

        try:
            # Convert user wallet address to checksum format
            user_wallet_checksum_address: ChecksumAddress = self.config.to_checksum_address(address=user_wallet_address)

            # Get the current nonce for the user’s wallet
            nonce: int = self.config.connection.eth.get_transaction_count(user_wallet_checksum_address)

            # Use the provided gas limits (or default to a safe estimate if not available)
            gas_estimate: int = gas_limits.get("gas_estimate", 2 * self._gas_limits_order_type_contract_function.call())
            max_fee_per_gas: int = gas_limits.get("max_fee_per_gas", int(self.max_fee_per_gas))
            max_priority_fee_per_gas: int = gas_limits.get("max_priority_fee_per_gas", 0)

            # Build the transaction using the provided gas limits
            raw_txn: TxParams = self._exchange_router_contract_obj.functions.multicall(
                multicall_args
            ).build_transaction(
                {
                    "value": value_amount,
                    "chainId": self.config.chain_id,
                    "gas": gas_estimate,
                    "maxFeePerGas": max_fee_per_gas,
                    "maxPriorityFeePerGas": max_priority_fee_per_gas,
                    "nonce": nonce,
                }
            )

            # Sign and submit the transaction if not in debug mode
            if not self.debug_mode:
                signed_txn: SignedTransaction = self.config.connection.eth.account.sign_transaction(
                    raw_txn, self.config.private_key
                )
                tx_hash: HexBytes = self.config.connection.eth.send_raw_transaction(signed_txn.rawTransaction)
                self.logger.info(f"Transaction submitted! Tx hash: {tx_hash.hex()}")

        except Exception as e:
            self.logger.error(f"Failed to submit transaction: {e}")
            raise Exception(f"Failed to submit transaction: {e}")

    def _check_initial_tokens(self) -> None:
        """
        Check and set long or short token addresses if they are not defined.

        :return: None.
        """
        for token_type, token_amount, token_key, token_name in [
            ("long", self.long_token_amount, "long_token_address", "initial_long_token"),
            ("short", self.short_token_amount, "short_token_address", "initial_short_token"),
        ]:
            if token_amount == 0:
                token_address: str = self.all_markets_info.get(self.market_key, {}).get(token_key)
                if not token_address:
                    raise ValueError(f"{token_type.capitalize()} token address is missing in the market info.")
                setattr(self, token_name, token_address)

    def _determine_swap_paths(self) -> None:
        """
        Determine the required swap paths for the long and short tokens if their current addresses differ from the
        market-defined ones.

        :return: None.
        """
        # Determine swap path for long token if needed
        for token_type, initial_token, market_token_key, swap_path_attr in [
            ("long", self.initial_long_token, "long_token_address", "long_token_swap_path"),
            ("short", self.initial_short_token, "short_token_address", "short_token_swap_path"),
        ]:
            market_token_address: str = self.all_markets_info[self.market_key][market_token_key]
            if market_token_address != initial_token:
                swap_path, _ = determine_swap_route(
                    config=self.config,
                    markets=self.all_markets_info,
                    in_token=initial_token,
                    out_token=market_token_address,
                )
                setattr(self, swap_path_attr, swap_path)

    def _create_order(self, arguments: tuple) -> HexBytes:
        """
        Create the encoded order using the exchange contract's ABI.

        :param arguments: A tuple containing the arguments required for creating a deposit order.
        :return: Encoded transaction in HexBytes format.
        """
        if not arguments:
            logging.error("Transaction arguments must not be empty.")
            raise ValueError("Transaction arguments must not be empty.")
        return self._exchange_router_contract_obj.functions.createDeposit.encodeABI([arguments])

    def _send_tokens(self, token_address: str, amount: int) -> HexBytes:
        """
        Send tokens to the exchange contract.

        :param token_address: The token address to send.
        :param amount: The amount of tokens to send.
        :return: Encoded transaction in HexBytes format.
        """
        if not token_address or amount <= 0:
            logging.error("Invalid token address or amount")
            raise ValueError("Invalid token address or amount")
        return self._exchange_router_contract_obj.functions.sendTokens.encodeABI(
            token_address, self.config.contracts.deposit_vault.contract_address, amount
        )

    def _send_wnt(self, amount: int) -> HexBytes:
        """
        Send WNT to the exchange contract.

        :param amount: The amount of WNT to send.
        :return: Encoded transaction in HexBytes format.
        """
        if amount <= 0:
            logging.error("WNT amount must be greater than zero.")
            raise ValueError("WNT amount must be greater than zero.")
        return self._exchange_router_contract_obj.functions.sendWnt.encodeABI(
            self.config.contracts.deposit_vault.contract_address, amount
        )

    def _estimate_deposit(self) -> int:
        """
        Estimate the amount of RM tokens based on deposit amounts and current token prices.

        :return: Estimated RM tokens out.
        """
        oracle_prices: dict[str, dict[str, Any]] = OraclePrices(config=self.config).get_recent_prices()

        # Extract market and token prices
        market_addresses, prices = self._get_market_data_and_prices(
            market=self.all_markets_info[self.market_key],
            oracle_prices=oracle_prices,
        )

        parameters: dict[str, Any] = {
            "data_store_address": self.config.contracts.data_store.contract_address,
            "market_addresses": market_addresses,
            "token_prices_tuple": prices,
            "long_token_amount": self.long_token_amount,
            "short_token_amount": self.short_token_amount,
            "ui_fee_receiver": self.config.zero_address,
        }

        return get_estimated_deposit_amount_out(config=self.config, params=parameters)

    def _get_market_data_and_prices(self, market: dict, oracle_prices: dict) -> tuple[list[str], list[tuple[int, int]]]:
        """
        Helper function to fetch market addresses and prices for the current market.

        :param market: Market information from all markets.
        :param oracle_prices: Dictionary of token prices fetched from Oracle.
        :return: A tuple containing market addresses and prices.
        """
        market_addresses = [
            self.market_key,
            market["index_token_address"],
            market["long_token_address"],
            market["short_token_address"],
        ]

        prices = [
            (int(oracle_prices[token]["minPriceFull"]), int(oracle_prices[token]["maxPriceFull"]))
            for token in [market["index_token_address"], market["long_token_address"], market["short_token_address"]]
        ]

        return market_addresses, prices
