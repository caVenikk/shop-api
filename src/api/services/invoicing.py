import json

import httpx
from fastapi import APIRouter, HTTPException, status
from httpx import ConnectError

from src.api.services import schema as sc

router = APIRouter(
    prefix="/create_invoice_link",
    tags=["invoice"],
)


async def create_invoice_link(product, user_id):
    try:
        data = dict(product=json.loads(product.json()), user_id=user_id)
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://127.0.0.1:8888/create_invoice_link",
                json=data
            )
        return response
    except ConnectError:
        pass


@router.post("/")
async def get_invoice_link(data: sc.ProductUserId):
    response = await create_invoice_link(data.product, data.user_id)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Cannot Call Bot Endpoint"
        )
    elif response.status_code == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product Not Found"
        )
    elif response.status_code == 500:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )
    return response.json()
