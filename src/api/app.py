from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.services import ROUTERS

app = FastAPI()
for router in ROUTERS:
    app.include_router(router)

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def root():
    return {'message': 'Hello World!'}
