from src.db.database import create_database_session
from src.utils import Singleton
from .base_repository import BaseRepository
from .order_repository import OrderRepository
from .product_repository import ProductRepository
from .user_repository import UserRepository


# Определение класса CRUD, который является синглтоном (только один экземпляр класса может существовать).
class CRUD(metaclass=Singleton):
    # В инициализаторе класса создается сессия базы данных с помощью create_database_session(). Затем создаются
    # экземпляры репозиториев UserRepository, ProductRepository и OrderRepository, передавая созданную сессию в
    # качестве аргумента. Эти экземпляры сохраняются в атрибутах класса.
    def __init__(self):
        session = create_database_session()
        self.users = UserRepository(session)
        self.products = ProductRepository(session)
        self.orders = OrderRepository(session)

    # Метод __call__ возвращает сам объект CRUD. Это позволяет вызывать экземпляр класса CRUD как функцию. Например,
    # если crud - экземпляр класса CRUD, то crud() будет возвращать сам crud. Это делается для удобства использования и
    # согласуется с паттерном проектирования "синглтон", где одиночный объект имеет функциональность, доступную через
    # вызов объекта как функции.
    def __call__(self):
        return self


# Запросы будут выглядеть следующим образом:
# products = await crud.products.all(limit, offset) - получение всех продуктов
# await crud.users.add(user=models.User(**new_user.dict())) - создание пользователя
