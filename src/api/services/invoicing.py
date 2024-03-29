import json

import httpx
from fastapi import APIRouter, HTTPException, status
from httpx import ConnectError

from src.api.services import schema as sc
from src.api.services.products.schema import ResponseProduct
from src.config import Config

router = APIRouter(
    prefix="/create_invoice_link",
    tags=["invoice"],
)


async def create_invoice_link(products: list[ResponseProduct], counters: list[str], user_id: int):
    try:
        config = Config.load()
        bot_host = config.bot.host if config.bot.host else "127.0.0.1"
        data = dict(products=[json.loads(product.json()) for product in products], counters=counters, user_id=user_id)
        async with httpx.AsyncClient() as client:
            response = await client.post(f"http://{bot_host}:8888/create_invoice_link", json=data)
        return response
    except ConnectError:
        pass


@router.post("/")
async def get_invoice_link(data: sc.ProductsUserId):
    response = await create_invoice_link(data.products, data.counters, data.user_id)
    if not response:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Cannot Call Bot Endpoint")
    elif response.status_code == 404:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product Not Found")
    elif response.status_code == 500:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    return response.json()
