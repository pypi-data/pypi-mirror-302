import json

from ...utils.exceptions import FileReadException, FILE_READ_ERROR


class ContractUtils:
    def __init__(self):
        pass

    @staticmethod
    def read_json_file(file_path: str) -> list[object]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        except json.JSONDecodeError as e:
            raise FileReadException(FILE_READ_ERROR)
