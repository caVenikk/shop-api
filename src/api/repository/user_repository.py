from sqlalchemy import select, update
from sqlalchemy.orm import sessionmaker

from src.api.repository import BaseRepository
from src.db import models as md


class UserRepository(BaseRepository):
    def __init__(self, session: sessionmaker):
        super().__init__(session)

    async def add(self, user: md.User):
        async with self._session() as s:
            async with s.begin():
                s.add(user)

    async def get(self, user_id: int) -> md.User | None:
        async with self._session() as s:
            return (await s.execute(select(md.User).where(md.User.id == user_id))).scalar()

    async def all(self, limit: int | None = None, offset: int | None = None) -> list[md.User]:
        async with self._session() as s:
            return (await s.execute(select(md.User).offset(offset).limit(limit))).scalars()

    async def update(self, user: md.User):
        async with self._session() as s:
            async with s.begin():
                update_user_stmt = (
                    update(md.User)
                    .where(md.User.id == user.id)
                    .values(first_name=user.first_name, second_name=user.second_name, username=user.username)
                )
                return bool((await s.execute(update_user_stmt)).rowcount)

    async def delete(self, user_id: int) -> bool:
        async with self._session() as s:
            async with s.begin():
                return bool(
                    (await s.execute(update(md.User).where(md.User.id == user_id).values(active=False))).rowcount
                )

    async def restore(self, user_id: int):
        async with self._session() as s:
            async with s.begin():
                return bool(
                    (await s.execute(update(md.User).where(md.User.id == user_id).values(active=True))).rowcount
                )
