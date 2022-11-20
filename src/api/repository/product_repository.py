from sqlalchemy import select, update, delete
from sqlalchemy.orm import sessionmaker

from src.api.repository import BaseRepository
from src.db import models as md


class ProductRepository(BaseRepository):
    def __init__(self, session: sessionmaker):
        super().__init__(session)

    async def add(self, product: md.Product):
        async with self._session() as s:
            async with s.begin():
                s.add(product)

    async def get(self, product_id: int) -> md.Product | None:
        async with self._session() as s:
            return (await s.execute(
                select(md.Product).where(md.Product.id == product_id)
            )).scalar()

    async def all(
            self,
            limit: int | None = None,
            offset: int | None = None
    ) -> list[md.Product]:
        async with self._session() as s:
            return (await s.execute(
                select(md.Product).offset(offset).limit(limit)
            )).scalars()

    async def update(self, product: md.Product):
        async with self._session() as s:
            async with s.begin():
                update_product_stmt = (
                    update(md.Product).
                    where(md.Product.id == product.id).
                    values(
                        title=product.title,
                        price=product.price,
                        weight=product.weight,
                        description=product.description
                    )
                )
                return bool((await s.execute(update_product_stmt)).rowcount)

    async def delete(self, product_id: int):
        async with self._session() as s:
            async with s.begin():
                return bool((await s.execute(
                    delete(md.Product).where(md.Product.id == product_id)
                )).rowcount)
