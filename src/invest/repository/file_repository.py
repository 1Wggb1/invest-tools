import json

from src.invest.repository.file_writter import FileWritter


class FileResultRepository:

    def __init__(self, file_name, file_result: FileWritter):
        self.file_name = file_name
        self.file_result = file_result

    def persist_all(self, results: str):
        self.file_result.override_write(self.file_name, results)

    def __find_result(self) -> dict:
        read_result = self.file_result.read(self.file_name)
        return json.loads(read_result) if len(read_result) else {}

