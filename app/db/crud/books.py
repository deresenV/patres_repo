from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.book import Book
from app.db.schemas.book import BookCreate, BookUpdate
from sqlalchemy.exc import NoResultFound, IntegrityError


async def create_book(db: AsyncSession, book_data: BookCreate) -> Book:
    new_book = Book(
        title=book_data.title,
        author=book_data.author,
        year=book_data.year,
        isbn=book_data.isbn,
        copy_versions=book_data.copy_versions
    )
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book


async def get_book(db: AsyncSession, book_id: int) -> Book:
    query = select(Book).where(Book.id == book_id)
    result = await db.execute(query)
    book = result.scalar_one_or_none()
    if not book:
        raise NoResultFound("Книга не найдена")
    return book


async def update_book(db: AsyncSession, book_id: int, book_data: BookUpdate) -> Book:
    book = await get_book(db, book_id)

    update_data = book_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(book, field, value)

    await db.commit()
    await db.refresh(book)
    return book


async def delete_book(db: AsyncSession, book_id: int) -> Book:
    book = await get_book(db, book_id)
    await db.delete(book)
    await db.commit()
    return book


async def get_all_books(db: AsyncSession) -> list[Book]:
    query = select(Book)
    result = await db.execute(query)
    return result.scalars().all()


async def get_books(db: AsyncSession):
    result = await db.execute(select(Book))
    return result.scalars().all()