from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from src.api.repository import CRUD
from src.api.services.orders import schema as sc
from src.db import models as md

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "model": list[sc.ResponseOrder],
            "description": "Orders array"
        }
    }
)
async def get_orders(limit: int | None = None, offset: int | None = None, crud: CRUD = Depends(CRUD)):
    orders = await crud.orders.all(limit, offset)
    return [sc.ResponseOrder.from_orm(order) for order in orders]


@router.get(
    "/{order_id}",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "model": sc.ResponseOrder,
            "description": "Order"
        },
        404: {"description": "Order not found"}
    }
)
async def get_order(order_id: int, crud: CRUD = Depends(CRUD)):
    order = await crud.orders.get(order_id=order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id={order_id} not found."
        )
    return sc.ResponseOrder.from_orm(order)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "model": sc.ResponseOrder,
            "description": "Order successfully created"
        },
        404: {"description": "Product not found"}
    }
)
async def add_order(order: sc.Order, crud: CRUD = Depends(CRUD)):
    new_order = md.Order(**order.dict())
    try:
        await crud.orders.add(order=new_order)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id={order.product_id} not found."
        )
    return sc.ResponseOrder.from_orm(new_order)


@router.delete(
    "/{order_id}",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Order deleted"},
        404: {"description": "Order not found"}
    }
)
async def delete_order(order_id: int, crud: CRUD = Depends(CRUD)):
    if not await crud.orders.delete(order_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id={order_id} not found."
        )
    return JSONResponse(
        content={"detail": f"Deleted order with id={order_id}."}
    )
