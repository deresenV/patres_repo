from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.crud.readers import create_reader, get_reader, update_reader, delete_reader
from app.db.schemas.reader import ReaderCreate, ReaderUpdate, Reader
from app.methods.token import get_current_user
from app.db.models.user import User
from sqlalchemy.exc import NoResultFound, IntegrityError

router = APIRouter(
    prefix="/readers",
    tags=["readers"]
)

@router.post("/create", response_model=Reader)
async def create_reader_endpoint(
    reader_data: ReaderCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        new_reader = await create_reader(db, reader_data)
        return new_reader
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")

@router.get("/{reader_id}", response_model=Reader)
async def get_reader_endpoint(
    reader_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        reader = await get_reader(db, reader_id)
        return reader
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Пользователь с id:{reader_id} не найден")

@router.put("/{reader_id}", response_model=Reader)
async def update_reader_endpoint(
    reader_id: int,
    reader_data: ReaderUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        reader = await update_reader(db, reader_id, reader_data)
        return reader
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Читатель не найден")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Читатель с таким email уже существует")

@router.delete("/{reader_id}", response_model=Reader)
async def delete_reader_endpoint(
    reader_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        reader = await delete_reader(db, reader_id)
        return reader
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Читатель не найден")