from functools import lru_cache

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.config import Config


@lru_cache(maxsize=1)
def create_database_session():
    config = Config.load()
    db_engine = create_async_engine(
        f"postgresql+asyncpg://{config.database.url}",
        echo=True,
        encoding='utf-8',
        future=True,
    )
    session = sessionmaker(
        bind=db_engine,
        expire_on_commit=False,
        class_=AsyncSession
    )
    return session
