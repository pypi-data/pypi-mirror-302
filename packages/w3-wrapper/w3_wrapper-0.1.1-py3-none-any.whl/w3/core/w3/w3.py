
from pydantic import validate_call, Field
from web3 import AsyncWeb3, AsyncHTTPProvider

from ...utils.exceptions import RPCException
from ...utils.regex import PROXY_REGEX
from ..async_mixin import AsyncMixin
from ..network import Network


class W3(AsyncMixin):

    @validate_call
    async def __ainit__(
            self,
            network: Network,
            proxy: str = Field(pattern=PROXY_REGEX)
    ) -> None:
        async_w3: AsyncWeb3 = AsyncWeb3(
            AsyncHTTPProvider(
                endpoint_uri=network.rpc,
                request_kwargs={"proxy": proxy},
            )
        )
        is_connected = await async_w3.is_connected()
        if is_connected:
            self.async_w3: AsyncWeb3 = async_w3
            self.network: Network = network
            self._proxy: str = proxy
        else:
            raise RPCException('RPC not working')
