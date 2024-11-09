import json
import os
from typing import Any, Dict, Optional

from . import Storage


class FilesStorage(Storage):
    def __init__(self, path: str):
        self.path = path
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def put(self, key: str, data: Any) -> None:
        with open(f"{self.path}/{key}", "wb") as file:
            file.write(data)

    def get(self, key: str) -> Optional[Any]:
        with open(f"{self.path}/{key}", "rb") as file:
            return file.read()

    def delete(self, key: str) -> None:
        os.remove(f"{self.path}/{key}")

    def clear(self) -> None:
        for file in os.listdir(self.path):
            os.remove(f"{self.path}/{file}")
