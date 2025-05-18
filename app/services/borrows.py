from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.borrowed_book import BorrowedBook
from app.db.crud.books import get_book
from app.db.crud.readers import get_reader
from sqlalchemy.exc import NoResultFound
from app.db.schemas.borrowed_book import BorrowedBookResponse

async def service_give_book(db: AsyncSession, book_id: int, reader_id: int):
    # Получаем книгу и читателя
    book = await get_book(db, book_id)
    reader = await get_reader(db, reader_id)
    
    if not book:
        raise NoResultFound(f"Книга с id:{book_id} не найдена")
    if not reader:
        raise NoResultFound(f"Читатель с id:{reader_id} не найден")
    
    # Проверяем доступность книги
    if book.copy_versions <= 0:
        raise ValueError("Нет доступных экземпляров книги")

    # Проверяем, не взял ли читатель уже эту книгу
    query = select(BorrowedBook).where(
        BorrowedBook.book_id == book_id,
        BorrowedBook.reader_id == reader_id,
        BorrowedBook.return_date.is_(None)
    )
    result = await db.execute(query)
    existing_borrow = result.scalar_one_or_none()
    if existing_borrow:
        raise ValueError(f"Читатель уже взял эту книгу")

    # Получаем количество взятых книг через запрос
    query = select(BorrowedBook).where(
        BorrowedBook.reader_id == reader_id,
        BorrowedBook.return_date.is_(None)
    )
    result = await db.execute(query)
    borrowed_books = result.scalars().all()
    borrowed_books_count = len(borrowed_books)

    if borrowed_books_count >= 3:
        raise ValueError(f"У читателя уже взято {borrowed_books_count} книг. Максимальное количество: 3")

    # Уменьшаем количество доступных экземпляров
    book.copy_versions -= 1

    # Создаем запись о взятии книги
    borrow_date = datetime.now()
    new_borrow = BorrowedBook(
        book_id=book_id,
        reader_id=reader_id,
        borrow_date=borrow_date,
        return_date=None
    )
    
    # Добавляем запись в БД
    db.add(new_borrow)
    
    # Сохраняем все изменения в одной транзакции
    await db.commit()
    await db.refresh(new_borrow)
    
    return new_borrow

async def service_return_book(db: AsyncSession, book_id: int, reader_id: int):
    # Получаем книгу и читателя
    book = await get_book(db, book_id)
    reader = await get_reader(db, reader_id)
    
    if not book:
        raise NoResultFound(f"Книга с id:{book_id} не найдена")
    if not reader:
        raise NoResultFound(f"Читатель с id:{reader_id} не найден")
    
    # Получаем все активные записи о взятии книги
    query = select(BorrowedBook).where(
        BorrowedBook.book_id == book_id,
        BorrowedBook.reader_id == reader_id,
        BorrowedBook.return_date.is_(None)
    )
    result = await db.execute(query)
    borrows = result.scalars().all()
    
    if not borrows:
        raise NoResultFound(f"Нет активных записей о взятии книги с id:{book_id} читателем с id:{reader_id}")
    
    # Устанавливаем время возврата
    return_date = datetime.now()
    
    # Обновляем все найденные записи
    for borrow in borrows:
        borrow.return_date = return_date
        db.add(borrow)  # Добавляем объект в сессию для обновления
    
    # Увеличиваем количество доступных экземпляров
    book.copy_versions += len(borrows)
    db.add(book)  # Добавляем книгу в сессию для обновления

    # Сохраняем изменения
    await db.commit()
    
    # Обновляем первый объект после коммита
    await db.refresh(borrows[0])
    
    # Возвращаем обновленный объект
    return BorrowedBookResponse.model_validate(borrows[0])

async def service_get_books_by_reader(db: AsyncSession, reader_id: int):
    query = select(BorrowedBook).where(
        BorrowedBook.reader_id == reader_id,
        BorrowedBook.return_date.is_(None)
    )
    result = await db.execute(query)
    borrowed_books = result.scalars().all()
    if len(borrowed_books) == 0:
        raise NoResultFound(f"Нет взятых книг читателем с id:{reader_id}")
    return borrowed_books