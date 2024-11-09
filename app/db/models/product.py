from pydantic import BaseModel


class Product(BaseModel):
    title: str  # title of the product
    price: float  # price of the product
    image_path: str  # path to the image of the product, located in data/images/ folder
