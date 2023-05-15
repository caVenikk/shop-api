from pydantic import BaseModel


class Order(BaseModel):
    user_id: int
    products_ids: list[int]
    counters: list[int]
    name: str
    phone_number: str
    country_code: str
    state: str | None = ""
    city: str
    street_line1: str
    street_line2: str | None = ""
    post_code: str
    total_amount: int


class ResponseOrder(BaseModel):
    id: int
    user_id: int
    name: str
    phone_number: str
    country_code: str
    state: str | None = ""
    city: str
    street_line1: str
    street_line2: str | None = ""
    post_code: str
    total_amount: int

    class Config:
        orm_mode = True
