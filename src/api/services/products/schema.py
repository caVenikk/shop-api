from pydantic import BaseModel


class Product(BaseModel):
    title: str
    price: float
    weight: float | None = None
    description: str | None = None


class ResponseProduct(Product):
    id: int
    active: bool

    class Config:
        orm_mode = True
