from pydantic import BaseModel

import src.api.services.products.schema as sc


class ProductsUserId(BaseModel):
    products: list[sc.ResponseProduct]
    user_id: int
