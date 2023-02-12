from src.db.database import create_database_session
from src.utils import Singleton
from .base_repository import BaseRepository
from .order_repository import OrderRepository
from .product_repository import ProductRepository
from .user_repository import UserRepository


class CRUD(metaclass=Singleton):
    def __init__(self):
        session = create_database_session()
        self.users = UserRepository(session)
        self.products = ProductRepository(session)
        self.orders = OrderRepository(session)

    def __call__(self):
        return self
