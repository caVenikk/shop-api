from sqlalchemy.orm import sessionmaker

from src.api.repository import BaseRepository
from src.db import models as md


class OrderRepository(BaseRepository):
    def __init__(self, session: sessionmaker):
        super().__init__(session)

    def add(self, order: md.Order):
        pass

    def get(self, order_id: int):
        pass

    def delete(self, order_id: int):
        pass
