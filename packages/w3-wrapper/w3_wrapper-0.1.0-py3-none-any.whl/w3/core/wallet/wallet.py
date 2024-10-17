from eth_typing import ChecksumAddress
from pydantic import BaseModel, Field, ConfigDict
from web3.contract import AsyncContract

from ...utils.regex import PRIVATE_KEY_REGEX, ADDRESS_REGEX
from ...utils.types import Contract
from ..contract import Contracts
from ..token_amount import TokenAmount
from ..w3 import W3


class Wallet(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    private_key: str = Field(pattern=PRIVATE_KEY_REGEX)
    public_key: str = Field(pattern=ADDRESS_REGEX)
    _w3: W3
    _contracts: Contracts

    def __init__(self, private_key: str, public_key: ChecksumAddress, w3: W3):
        super(Wallet, self).__init__(
            private_key=private_key,
            public_key=public_key,
        )
        self._w3 = w3
        self._contracts = Contracts(w3)

    async def get_balance(self, token: Contract = None) -> TokenAmount:
        if token is None:
            return TokenAmount(
                await self._w3.async_w3.eth.get_balance(
                    account=self._w3.async_w3.to_checksum_address(self.public_key)
                ),
                18
            )
        token_address = self._w3.async_w3.to_checksum_address(token)
        if isinstance(token, AsyncContract):
            token_address = token.address

        contract = self._contracts.get_erc20_contract(token_address)
        return TokenAmount(
            int(await contract.functions.balanceOf(self.public_key).call()),
            int(await contract.functions.decimals().call())
        )
