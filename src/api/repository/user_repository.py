from sqlalchemy.orm import sessionmaker

from src.api.repository import BaseRepository
from src.db import models as md


class UserRepository(BaseRepository):
    def __init__(self, session: sessionmaker):
        super().__init__(session)

    def add(self, user: md.User):
        pass

    def get(self, user_id: int):
        pass

    def delete(self, user_id: int):
        pass
