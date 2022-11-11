from fastapi import FastAPI

from src.api.services import ROUTERS

app = FastAPI()
for router in ROUTERS:
    app.include_router(router)


@app.get('/')
async def root():
    return {'message': 'Hello World!'}
