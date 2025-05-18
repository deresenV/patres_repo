import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.db.database import Base
from app.methods.token import create_access_token
from app.db.models.user import User
from app.db.models.book import Book
from app.db.models.reader import Reader
from app.methods.utils import hash_password

# Создаем тестовую базу данных в памяти
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture
async def test_db():
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        yield session

@pytest_asyncio.fixture
async def test_user(test_db):
    user = User(
        email="test@example.com",
        hashed_password=hash_password("testpassword")
    )
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    return user

@pytest_asyncio.fixture
async def test_token(test_user):
    return create_access_token({"sub": test_user.email})

@pytest_asyncio.fixture
async def test_book(test_db):
    book = Book(
        title="Test Book",
        author="Test Author",
        year=2024,
        isbn="1234567890",
        copy_versions=3
    )
    test_db.add(book)
    await test_db.commit()
    await test_db.refresh(book)
    return book

@pytest_asyncio.fixture
async def test_reader(test_db):
    reader = Reader(
        email="reader@example.com",
        name="Test Reader"
    )
    test_db.add(reader)
    await test_db.commit()
    await test_db.refresh(reader)
    return reader 