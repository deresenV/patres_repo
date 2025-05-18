from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import config
from app.db.crud.users import create_user, get_user
from app.db.database import get_db
from app.db.schemas.user import UserCreate
from app.methods.token import create_access_token
from app.methods.utils import verify_password

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


@auth_router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user = await get_user(form_data.username, db)
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не найден")

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Пароль введен неверно")

    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {"access_token": access_token, "token_type": "bearer"}