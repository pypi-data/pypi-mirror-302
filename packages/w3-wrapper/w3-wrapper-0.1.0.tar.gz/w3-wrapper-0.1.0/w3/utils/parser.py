class Parser:
    def __init__(self):
        pass

    @staticmethod
    def printParsedContractData(data: str):
        signature: str = data[:10]
        data = data[10:]
        print(signature)
        while len(data) > 0:
            print(data[:64])
            data = data[64:]
