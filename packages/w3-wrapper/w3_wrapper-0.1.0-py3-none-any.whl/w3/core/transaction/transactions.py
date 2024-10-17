from eth_account.datastructures import SignedTransaction
from eth_typing import HexStr, ChecksumAddress
from hexbytes import HexBytes
from pydantic import validate_call
from web3.types import TxReceipt

from ..gas_strategy import OldGasStrategy, EIP1559GasStrategy, GasStrategy
from ..w3 import W3
from ..wallet import Wallet


class Transactions:
    def __init__(self, w3: W3, wallet: Wallet) -> None:
        self._w3: W3 = w3
        self._wallet: Wallet = wallet
        if self._w3.network.tx_type == 0:
            self._gas_strategy: GasStrategy = OldGasStrategy(self._w3)
        else:
            self._gas_strategy: GasStrategy = EIP1559GasStrategy(self._w3)

    async def _create_transaction(
            self,
            contract_address: ChecksumAddress,
            encoded_data: HexStr,
            value: int,
    ) -> dict:
        gas_dict = await self._gas_strategy.calculate_gas()
        raw_tx = {
            'chainId': self._w3.network.chain_id,
            'nonce': await self._w3.async_w3.eth.get_transaction_count(self._wallet.public_key),
            'from': self._wallet.public_key,
            'to': contract_address,
            'data': encoded_data,
            'value': value,
        }
        tx = dict(raw_tx, **gas_dict)
        return tx

    async def _estimate_gas(self, tx: dict) -> dict:
        tx_copy = tx.copy()
        tx_copy['gas'] = await self._w3.async_w3.eth.estimate_gas(tx_copy)
        return tx_copy

    def _sign_transaction(self, tx: dict) -> SignedTransaction:
        return self._w3.async_w3.eth.account.sign_transaction(tx, private_key=self._wallet.private_key)

    async def _wait_for_receipt(self, tx_hash) -> TxReceipt:
        tx_receipt = await self._w3.async_w3.eth.wait_for_transaction_receipt(tx_hash, 300)
        return tx_receipt

    async def _send_raw_transaction(self, tx: SignedTransaction) -> HexBytes:
        return await self._w3.async_w3.eth.send_raw_transaction(tx.raw_transaction)

    @validate_call
    async def send(
            self,
            contract_address: ChecksumAddress,
            encoded_data: HexStr,
            tx_value: int = 0,
            retry_count: int = 5,
    ) -> TxReceipt:
        tx = await self._create_transaction(
            contract_address,
            encoded_data,
            tx_value,
        )
        for i in range(retry_count):
            tx = await self._estimate_gas(tx)
            signed_tx: SignedTransaction = self._sign_transaction(tx)
            tx_hash: HexBytes = await self._send_raw_transaction(signed_tx)
            res = await self._wait_for_receipt(tx_hash)
            if res.get('status') == 1:
                return res
            else:
                cf: float = 1 + (5 + retry_count) / 100
                if 'gasPrice' in tx:
                    tx['gasPrice'] = int(tx['gasPrice'] * cf)
                else:
                    tx['maxFeePerGas'] = int(tx['maxFeePerGas'] * cf)
                    tx['maxPriorityFeePerGas'] = int(tx['maxPriorityFeePerGas'] * cf)
