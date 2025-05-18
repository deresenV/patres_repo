from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.db.models.borrowed_book import BorrowedBook
from app.db.models.book import Book
from app.db.models.reader import Reader
from app.db.schemas.borrowed_book import BorrowedBookBase, BorrowedBookResponse, BorrowedBookCreate, BorrowedBookReturn
from app.methods.token import get_current_user
from app.services.borrows import (service_give_book,
                              service_return_book,
                              service_get_books_by_reader)
from sqlalchemy.exc import NoResultFound
from app.db.models.user import User

router = APIRouter(
    prefix="/borrows",
    tags=["borrows"]
)

@router.post("/give", response_model=BorrowedBookResponse)
async def give_book_endpoint(
    borrow_data: BorrowedBookCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return await service_give_book(db, borrow_data.book_id, borrow_data.reader_id)
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/return", response_model=BorrowedBookResponse)
async def return_book_endpoint(
    borrow_data: BorrowedBookBase,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return await service_return_book(db, borrow_data.book_id, borrow_data.reader_id)
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except:
        raise HTTPException(status_code=400, detail="Ошибка")

@router.get("/{reader_id}/books", response_model=list[BorrowedBookResponse])
async def get_books_by_reader_endpoint(
    reader_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return await service_get_books_by_reader(db, reader_id)
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail=str(e))