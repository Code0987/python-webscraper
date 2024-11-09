from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class Storage(ABC):
    @abstractmethod
    def clear(self) -> None:
        pass
