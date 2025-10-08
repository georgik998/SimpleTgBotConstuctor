from typing import TypedDict, get_type_hints
import json
import os


class JsonBaseRepo:
    dir_path: str
    model: TypedDict

    def model_type_matching(self, data) -> bool:
        if data is None:
            return False
        for field, field_type in get_type_hints(self.model).items():
            if field not in data:
                return False
            if not isinstance(data[field], field_type):
                return False
        return True

    @staticmethod
    def _write(data, file_path: str):
        with open(file_path, 'w') as f:
            json.dump(data, f)

    @staticmethod
    def _get(file_path: str):
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None

    @staticmethod
    def _delete(file_path: str):
        try:
            os.remove(file_path)
            return True
        except FileNotFoundError:
            return False
