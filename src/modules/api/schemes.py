from pydantic import BaseModel


class CreateProductModel(BaseModel):
    name: str
    url: str
    price: int


class UpdateProductModel(BaseModel):
    name: str | None = None
    url: str | None = None
    price: int | None = None


class ProductModel(BaseModel):
    id: int
    name: str
    url: str
    price: int
