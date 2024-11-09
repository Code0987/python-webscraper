from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class ProductsScrapper(ABC):
    @abstractmethod
    def scrape(self) -> list["Product"]:
        pass
