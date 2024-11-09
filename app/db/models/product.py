from pydantic import BaseModel
from typing import Union


class Product(BaseModel):
    title: str
    price: Union[float, int]
    image_path: str
