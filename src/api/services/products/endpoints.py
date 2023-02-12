from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse

from src.api.repository import CRUD
from src.api.services.products import schema as sc
from src.db import models as md

router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "model": list[sc.ResponseProduct],
            "description": "Products array"
        }
    }
)
async def get_products(
        limit: int | None = None,
        offset: int | None = None,
        crud: CRUD = Depends(CRUD)
):
    products = await crud.products.all(limit, offset)
    return [sc.ResponseProduct.from_orm(product) for product in products]


@router.get(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "model": sc.ResponseProduct,
            "description": "Product"
        },
        404: {"description": "Product not found"}
    }
)
async def get_product(product_id: int, crud: CRUD = Depends(CRUD)):
    product = await crud.products.get(product_id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id={product_id} not found."
        )
    return sc.ResponseProduct.from_orm(product)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "model": sc.ResponseProduct,
            "description": "Product successfully created"
        }
    }
)
async def add_product(product: sc.Product, crud: CRUD = Depends(CRUD)):
    new_product = md.Product(**product.dict())
    await crud.products.add(product=new_product)
    return sc.ResponseProduct.from_orm(new_product)


@router.put(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "model": sc.ResponseProduct,
            "description": "Product successfully updated"
        },
        404: {"description": "Product not found"}
    }
)
async def update_product(
        product_id: int,
        new_product: sc.Product,
        crud: CRUD = Depends(CRUD)
):
    updated_product = md.Product(
        id=product_id,
        **new_product.dict()
    )
    if not await crud.products.update(product=updated_product):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id={product_id} not found."
        )
    return sc.ResponseProduct.from_orm(updated_product)


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Product now inactive"},
        404: {"description": "Product not found"}
    }
)
async def delete_product(product_id: int, crud: CRUD = Depends(CRUD)):
    if not await crud.products.delete(product_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id={product_id} not found."
        )
    return JSONResponse(
        content={"detail": f"Product with id={product_id} now inactive."}
    )


@router.patch(
    "/{product_id}/restore",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Product restored"},
        404: {"description": "Product not found"}
    }
)
async def restore_product(product_id: int, crud: CRUD = Depends(CRUD)):
    if not await crud.products.restore(product_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id={product_id} not found."
        )
    return JSONResponse(
        content={"detail": f"Restored product with id={product_id}."}
    )
