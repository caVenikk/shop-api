from sqlalchemy.orm import sessionmaker

from src.api.repository import BaseRepository
from src.db import models as md


class ProductRepository(BaseRepository):
    def __init__(self, session: sessionmaker):
        super().__init__(session)

    def add(self, product: md.Product):
        pass

    def get(self, product_id: int):
        pass

    def update(self, product_id: int, product: md.Product):
        pass

    def delete(self, product_id: int):
        pass

