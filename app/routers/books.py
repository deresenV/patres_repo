from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.crud.books import create_book, get_book, get_books, update_book, delete_book
from app.db.schemas.book import BookCreate, BookUpdate, Book
from app.methods.token import get_current_user
from app.db.models.user import User
from sqlalchemy.exc import IntegrityError, NoResultFound

router = APIRouter(
    prefix="/books",
    tags=["books"]
)

@router.post("/create", response_model=Book)
async def create_book_endpoint(
    book_data: BookCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    '''Создание книги'''

    try:
        new_book = await create_book(db, book_data)
        return new_book
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Книга с таким ISBN уже существует")

@router.get("/all_books", response_model=list[Book])
async def get_all_books(
    db: AsyncSession = Depends(get_db)
):
    '''Получить все книги'''
    try:
        books = await get_books(db)
        return books
    except NoResultFound as e:
        raise HTTPException(status_code=200, detail=str(e))

@router.get("/{book_id}", response_model=Book)
async def get_book_endpoint(
    book_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    '''Получение книги'''
    try:
        book = await get_book(db, book_id)
        return book
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Книга не найдена")

@router.put("/{book_id}", response_model=Book)
async def update_book_endpoint(
    book_id: int,
    book_data: BookUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    '''Обновление полей книги'''
    try:
        book = await update_book(db, book_id, book_data)
        return book
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Книга с таким ISBN уже существует")

@router.delete("/{book_id}", response_model=Book)
async def delete_book_endpoint(
    book_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    '''Удаление книги по id'''
    try:
        book = await delete_book(db, book_id)
        return book
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Книга не найдена")