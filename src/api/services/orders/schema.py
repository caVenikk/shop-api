from pydantic import BaseModel


class Order(BaseModel):
    user_id: int
    product_id: int


class ResponseOrder(Order):
    id: int

    class Config:
        orm_mode = True
