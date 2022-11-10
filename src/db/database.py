from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import Config


@lru_cache(maxsize=1)
def create_database_session():
    config = Config.load()
    db_engine = create_engine(
        f"postgresql+asyncpg://{config.database.url}",
        echo=True, encoding='utf-8'
    )
    session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    return session
