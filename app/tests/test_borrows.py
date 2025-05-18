import pytest
import pytest_asyncio
from app.services.borrows import service_give_book, service_return_book
from app.db.models.book import Book
from sqlalchemy.exc import NoResultFound

@pytest.mark.asyncio
async def test_give_book_success(test_db, test_book, test_reader):
    # Тест успешной выдачи книги
    result = await service_give_book(test_db, test_book.id, test_reader.id)
    assert result.book_id == test_book.id
    assert result.reader_id == test_reader.id

@pytest.mark.asyncio
async def test_give_book_no_copies(test_db, test_book, test_reader):
    # Тест выдачи книги без доступных копий
    test_book.copy_versions = 0
    test_db.add(test_book)
    await test_db.commit()
    
    with pytest.raises(ValueError) as exc_info:
        await service_give_book(test_db, test_book.id, test_reader.id)
    assert "Нет доступных экземпляров книги" in str(exc_info.value)

@pytest_asyncio.fixture
async def test_book2(test_db):
    book = Book(
        title="Test Book 2",
        author="Test Author 2",
        year=2024,
        isbn="0987654321",
        copy_versions=3
    )
    test_db.add(book)
    await test_db.commit()
    await test_db.refresh(book)
    return book

@pytest_asyncio.fixture
async def test_books(test_db):
    books = []
    for i in range(4):
        book = Book(
            title=f"Test Book {i+1}",
            author=f"Test Author {i+1}",
            year=2024,
            isbn=f"123456789{i}",
            copy_versions=3
        )
        test_db.add(book)
        books.append(book)
    
    await test_db.commit()
    
    for book in books:
        await test_db.refresh(book)
    return books

@pytest.mark.asyncio
async def test_give_book_max_borrows(test_db, test_books, test_reader):
    # Тест выдачи книги при максимальном количестве взятых книг
    # Создаем максимальное количество записей о взятых книгах
    for i in range(3):
        await service_give_book(test_db, test_books[i].id, test_reader.id)
    
    with pytest.raises(ValueError) as exc_info:
        await service_give_book(test_db, test_books[3].id, test_reader.id)
    assert "У читателя уже взято 3 книг" in str(exc_info.value)

@pytest.mark.asyncio
async def test_return_book_success(test_db, test_book, test_reader):
    # Тест успешного возврата книги
    # Сначала выдаем книгу
    await service_give_book(test_db, test_book.id, test_reader.id)
    
    # Затем возвращаем её
    result = await service_return_book(test_db, test_book.id, test_reader.id)
    assert result.book_id == test_book.id
    assert result.reader_id == test_reader.id
    assert result.return_date is not None

@pytest.mark.asyncio
async def test_return_book_not_borrowed(test_db, test_book, test_reader):
    # Тест попытки вернуть книгу, которая не была взята
    with pytest.raises(NoResultFound) as exc_info:
        await service_return_book(test_db, test_book.id, test_reader.id)
    assert "Нет активных записей о взятии книги" in str(exc_info.value)

@pytest.mark.asyncio
async def test_give_book_already_borrowed(test_db, test_book, test_reader):
    # Тест попытки взять книгу, которая уже взята
    # Сначала берем книгу
    await service_give_book(test_db, test_book.id, test_reader.id)
    
    # Пытаемся взять ту же книгу снова
    with pytest.raises(ValueError) as exc_info:
        await service_give_book(test_db, test_book.id, test_reader.id)
    assert "Читатель уже взял эту книгу" in str(exc_info.value)

@pytest.mark.asyncio
async def test_return_book_invalid_data(test_db, test_book, test_reader):
    # Тест попытки вернуть книгу с неверными данными
    # Создаем несуществующего читателя
    with pytest.raises(NoResultFound) as exc_info:
        await service_return_book(test_db, test_book.id, 99999)
    assert "Читатель с id:99999 не найден" in str(exc_info.value)
    
    # Создаем несуществующую книгу
    with pytest.raises(NoResultFound) as exc_info:
        await service_return_book(test_db, 99999, test_reader.id)
    assert "Книга не найдена" in str(exc_info.value)