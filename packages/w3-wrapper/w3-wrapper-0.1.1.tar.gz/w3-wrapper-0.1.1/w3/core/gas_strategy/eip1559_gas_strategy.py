import statistics

from ..gas_strategy.gas_strategy import GasStrategy


class EIP1559GasStrategy(GasStrategy):
    async def calculate_gas(self) -> dict:
        block = await self._w3.async_w3.eth.get_block('latest')
        block_number = block['number']
        latest_block_transaction_count = await self._w3.async_w3.eth.get_block_transaction_count(block_number)
        max_fee_per_gas_list = []
        max_priority_fee_per_gas_list = []
        for i in range(latest_block_transaction_count):
            try:
                transaction = await self._w3.async_w3.eth.get_transaction_by_block(block_number, i)
                if 'maxPriorityFeePerGas' in transaction:
                    max_priority_fee_per_gas_list.append(transaction['maxPriorityFeePerGas'])
                if 'maxFeePerGas' in transaction:
                    max_fee_per_gas_list.append(transaction['maxFeePerGas'])
            except Exception:
                continue
        if not (max_priority_fee_per_gas_list or max_fee_per_gas_list):
            return {
                'maxFeePerGas': int(await self._w3.async_w3.eth.max_priority_fee),
                'maxPriorityFeePerGas': int(await self._w3.async_w3.eth.max_priority_fee / 10)
            }
        else:
            max_priority_fee_per_gas_list.sort()
            max_fee_per_gas_list.sort()
            return {
                'maxFeePerGas': int(statistics.median(max_fee_per_gas_list)),
                'maxPriorityFeePerGas': int(statistics.median(max_priority_fee_per_gas_list))
            }
