from __future__ import annotations

from ..async_mixin import AsyncMixin
from ..contract import Contracts
from ..network import Network
from ..transaction import Transactions
from ..w3 import W3
from ..wallet import Wallet


class Client(AsyncMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def __ainit__(self, private_key: str, network: Network, proxy: str) -> None:
        self.w3 = await W3(
            network,
            proxy
        )
        self.wallet = Wallet(
            private_key,
            self.w3.async_w3.eth.account.from_key(private_key).address,
            self.w3
        )
        self.transactions = Transactions(self.w3, self.wallet)
        self.contracts = Contracts(self.w3)

    async def switch_network(self, network: Network) -> Client:
        return await Client(self.wallet.private_key, network, self.w3._proxy)
        
