from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import AsyncGenerator

from app.config import config


# Создание асинхронного движка
engine = create_async_engine(config.SQLALCHEMY_DATABASE_URL, echo = True)

# Создание фабрики асинхронных сессий
AsyncSessionLocal = sessionmaker(
    bind = engine,
    class_= AsyncSession,
    expire_on_commit = False
)

# Базовый класс для моделей
Base = declarative_base()
from app.db.models import Book, BorrowedBook, Reader
# Генератор сессий
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session