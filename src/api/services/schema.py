from pydantic import BaseModel

import src.api.services.products.schema as sc


class ProductsUserId(BaseModel):
    products: list[sc.ResponseProduct]
    counters: list[str]
    user_id: int
