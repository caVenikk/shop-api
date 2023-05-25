from functools import lru_cache

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.config import Config


# Определение функции create_database_session(). Декоратор @lru_cache используется для кеширования результатов этой
# функции, чтобы избежать повторного создания сессии базы данных. Параметр maxsize=1 устанавливает то, что сессия может
# быть только одной (то есть функция выполнится один раз, после чего будет возвращать ту же сессию).
@lru_cache(maxsize=1)
def create_database_session():
    # Загрузка конфигурации базы данных с помощью метода load() класса Config. Этот метод загружает настройки из
    # конфигурационного файла.
    config = Config.load()
    # Создание асинхронного движка базы данных с помощью функции create_async_engine(). Указывается URL базы данных
    # (для PostgreSQL), извлеченный из конфигурации. Аргументы echo=True и encoding='utf-8' устанавливают вывод в
    # консоль SQL-запросов для отладки и кодировку символов соответственно. Аргумент future=True включает поддержку
    # новых функций, в том числе асинхронных операций (с выходом SQLAlchemy 2.0 данный параметр не требуется).
    db_engine = create_async_engine(
        f"postgresql+asyncpg://{config.database.url}",
        echo=True,
        encoding="utf-8",
        future=True,
    )
    # Создание фабрики сессий базы данных с помощью функции sessionmaker(). Устанавливается связь с асинхронным движком
    # db_engine. Аргумент expire_on_commit=False отключает автоматическую сессию после фиксации транзакции. Аргумент
    # class_=AsyncSession указывает, что используется асинхронная сессия.
    session = sessionmaker(bind=db_engine, expire_on_commit=False, class_=AsyncSession)
    # Возвращается фабрика сессий базы данных. Это позволяет вызывающему коду создавать и использовать сессии для
    # выполнения операций с базой данных.
    return session
