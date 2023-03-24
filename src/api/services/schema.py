from pydantic import BaseModel

import src.api.services.products.schema as sc


class ProductUserId(BaseModel):
    product: sc.ResponseProduct
    user_id: int
