from datetime import datetime

from pydantic import BaseModel


class Order(BaseModel):
    user_id: int
    product_id: int
    name: str
    phone_number: str
    country_code: str
    state: str | None = ""
    city: str
    street_line1: str
    street_line2: str | None = ""
    post_code: str
    total_amount: int
    ordered_at: datetime


class ResponseOrder(Order):
    id: int

    class Config:
        orm_mode = True
