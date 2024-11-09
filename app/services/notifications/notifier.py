from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class Notifier(ABC):
    @abstractmethod
    def notify(self, *args, **kwargs) -> None:
        pass
