from fastapi import FastAPI, Depends

from src.api.repository import CRUD
from src.api.services.users import schema as sc

app = FastAPI()


@app.get('/')
async def root(crud: CRUD = Depends(CRUD)):
    return {'message': 'Hello World!'}


@app.post('/')
async def root(user: sc.User, crud: CRUD = Depends(CRUD)):
    return {'message': 'Hello World!'}
