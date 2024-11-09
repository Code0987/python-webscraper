import json
import os
from typing import Any, Dict, Optional

from . import Storage


class JsonArrayFileStorage(Storage):
    '''
    This class is used to store data in a JSON file, in the form of a list of dictionaries.
    It provides methods to put, get, delete, and clear data from the JSON file.
    '''

    def __init__(self, filename: str):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as file:
                json.dump([], file)

    def _read_data(self) -> list[Dict[str, Any]]:
        with open(self.filename, "r") as file:
            return json.load(file)

    def _write_data(self, data: list[Dict[str, Any]]) -> None:
        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)

    def put(self, key_name: str, key_value: str, data: Any) -> None:
        all_data = self._read_data()
        updated_index = next(
            (i for i, d in enumerate(all_data) if d[key_name] == key_value), -1
        )
        if updated_index != -1:
            all_data[updated_index] = data
        else:
            all_data.append(data)
        self._write_data(all_data)

    def get(self, key_name: str, key_value: str) -> Optional[dict[str, any]]:
        all_data = self._read_data()
        return next((d for d in all_data if d[key_name] == key_value), None)

    def get_all(self, key_name: str, key_value: str) -> list[dict[str, any]]:
        return self._read_data()

    def delete(self, key: str) -> None:
        all_data = self._read_data()
        delete_index = next(
            (i for i, d in enumerate(all_data) if d[key_name] == key_value), -1
        )
        if delete_index != -1:
            del all_data[delete_index]
            self._write_data(all_data)

    def clear(self) -> None:
        self._write_data([])
