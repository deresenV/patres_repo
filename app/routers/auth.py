from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud.users import create_user
from app.db.database import get_db
from app.db.schemas.user import UserCreate

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"])


@auth_router.post("/register")
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        user = await create_user(db, user_data.email, user_data.password)
        return {"message": "Пользователь успешно создан", "user": user}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))