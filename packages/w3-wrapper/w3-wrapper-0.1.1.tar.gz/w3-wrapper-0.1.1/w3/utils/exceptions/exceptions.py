class SonicException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class WalletException(SonicException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class TransactionException(SonicException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class ContractException(SonicException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class FileReadException(SonicException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class RPCException(Exception):
    pass
