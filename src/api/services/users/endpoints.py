from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse

from src.api.repository import CRUD
from src.api.services.users import schema as sc
from src.db import models as md

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "model": list[sc.ResponseUser],
            "description": "Users array"
        }
    }
)
async def get_users(limit: int | None = None, offset: int | None = None, crud: CRUD = Depends(CRUD)):
    users = await crud.users.all(limit, offset)
    return [sc.ResponseUser.from_orm(user) for user in users]


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "model": sc.ResponseUser,
            "description": "User"
        },
        404: {"description": "User not found"}
    }
)
async def get_user(user_id: int, crud: CRUD = Depends(CRUD)):
    user = await crud.users.get(user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id={user_id} not found."
        )
    return sc.ResponseUser.from_orm(user)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "model": sc.ResponseUser,
            "description": "User successfully created"
        }
    }
)
async def add_user(user: sc.User, crud: CRUD = Depends(CRUD)):
    new_user = md.User(**user.dict())
    await crud.users.add(user=new_user)
    return sc.ResponseUser.from_orm(new_user)


@router.put(
    "/",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "model": sc.ResponseUser,
            "description": "User successfully updated"
        },
        404: {"description": "User not found"}
    }
)
async def update_user(
        new_user: sc.User,
        crud: CRUD = Depends(CRUD)
):
    updated_user = md.User(**new_user.dict())
    if not await crud.users.update(user=updated_user):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id={new_user.id} not found."
        )
    return sc.ResponseUser.from_orm(updated_user)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "User now inactive"},
        404: {"description": "User not found"}
    }
)
async def delete_user(user_id: int, crud: CRUD = Depends(CRUD)):
    if not await crud.users.delete(user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id={user_id} not found."
        )
    return JSONResponse(
        content={"detail": f"User with id={user_id} now inactive."}
    )


@router.patch(
    "/{user_id}/restore",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "User restored"},
        404: {"description": "User not found"}
    }
)
async def delete_user(user_id: int, crud: CRUD = Depends(CRUD)):
    if not await crud.users.restore(user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id={user_id} not found."
        )
    return JSONResponse(
        content={"detail": f"Restored user with id={user_id}."}
    )
