from sqlalchemy import select, delete, func
from sqlalchemy.orm import sessionmaker

from src.api.repository import BaseRepository
from src.db import models as md


class OrderRepository(BaseRepository):
    def __init__(self, session: sessionmaker):
        super().__init__(session)

    async def add(self, order: md.Order):
        async with self._session() as s:
            async with s.begin():
                s.add(order)

    async def get(self, order_id: int) -> md.Order | None:
        async with self._session() as s:
            return (await s.execute(
                select(md.Order).where(md.Order.id == order_id)
            )).scalar()

    async def get_last_id(self) -> int | None:
        async with self._session() as s:
            return (await s.execute(
                func.max(md.Order.id)
            )).scalar()

    async def all(
            self,
            limit: int | None = None,
            offset: int | None = None
    ) -> list[md.Order]:
        async with self._session() as s:
            return (await s.execute(
                select(md.Order).offset(offset).limit(limit)
            )).scalars()

    async def delete(self, order_id: int):
        async with self._session() as s:
            async with s.begin():
                return bool((await s.execute(
                    delete(md.Order).where(md.Order.id == order_id)
                )).rowcount)
