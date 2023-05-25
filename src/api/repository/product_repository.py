from sqlalchemy import select, update
from sqlalchemy.orm import sessionmaker

from src.api.repository import BaseRepository
from src.db import models as md


# Определение класса ProductRepository, который наследуется от BaseRepository. В инициализаторе класса вызывается
# инициализатор родительского класса, BaseRepository, с передачей аргумента session.
class ProductRepository(BaseRepository):
    def __init__(self, session: sessionmaker):
        super().__init__(session)

    # Метод add асинхронно добавляет новый продукт в базу данных. Создается асинхронная сессия с использованием
    # self._session(). Затем сессия оборачивается в блок async with и начинается транзакция с помощью s.begin().
    # Затем объект product добавляется в сессию с помощью s.add().
    async def add(self, product: md.Product):
        async with self._session() as s:
            async with s.begin():
                s.add(product)

    # Метод get асинхронно извлекает продукт по его идентификатору из базы данных. Создается асинхронная сессия с
    # использованием self._session(). Затем выполняется запрос select, чтобы выбрать продукт, соответствующий заданному
    # идентификатору, используя s.execute(). Затем вызывается scalar(), чтобы получить скалярное значение из результата
    # запроса.
    async def get(self, product_id: int) -> md.Product | None:
        async with self._session() as s:
            return (await s.execute(select(md.Product).where(md.Product.id == product_id))).scalar()

    # Метод all асинхронно извлекает все продукты из базы данных. Создается асинхронная сессия с использованием
    # self._session(). Затем выполняется запрос select, чтобы выбрать все продукты, используя s.execute(). Затем
    # вызывается scalars(), чтобы получить результат запроса в виде списка скалярных значений.
    async def all(self, limit: int | None = None, offset: int | None = None) -> list[md.Product]:
        async with self._session() as s:
            return (await s.execute(select(md.Product).offset(offset).limit(limit))).scalars()

    # Метод update асинхронно обновляет информацию о продукте в базе данных. Создается асинхронная сессия с
    # использованием self._session(). Затем выполняется запрос update, чтобы обновить информацию о продукте,
    # используя s.execute(). Результатом запроса является количество обновленных строк, которое возвращается в виде
    # булевого значения.
    async def update(self, product: md.Product):
        async with self._session() as s:
            async with s.begin():
                update_product_stmt = (
                    update(md.Product)
                    .where(md.Product.id == product.id)
                    .values(
                        title=product.title, price=product.price, weight=product.weight, description=product.description
                    )
                )
                return bool((await s.execute(update_product_stmt)).rowcount)

    # Метод delete асинхронно удаляет продукт из базы данных. Создается асинхронная сессия с использованием
    # self._session(). Затем выполняется запрос update, чтобы пометить продукт как неактивный, используя s.execute().
    # Результатом запроса является количество обновленных строк, которое возвращается в виде булевого значения
    # (изменилась ли хоть одна строка или нет).
    async def delete(self, product_id: int):
        async with self._session() as s:
            async with s.begin():
                return bool(
                    (
                        await s.execute(update(md.Product).where(md.Product.id == product_id).values(active=False))
                    ).rowcount
                )

    # Метод restore асинхронно восстанавливает удаленный продукт в базе данных. Создается асинхронная сессия с
    # использованием self._session(). Затем выполняется запрос update, чтобы пометить продукт как активный, используя
    # s.execute(). Результатом запроса является количество обновленных строк, которое возвращается в виде булевого
    # значения (изменилась ли хоть одна строка или нет).
    async def restore(self, product_id: int):
        async with self._session() as s:
            async with s.begin():
                return bool(
                    (
                        await s.execute(update(md.Product).where(md.Product.id == product_id).values(active=True))
                    ).rowcount
                )
