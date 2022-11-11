from .orders import router as orders_router
from .products import router as products_router
from .users import router as users_router

ROUTERS = [
    products_router,
    # users_router,
    # orders_router
]
