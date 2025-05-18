from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from app.methods.utils import hash_password


async def create_user(db: AsyncSession, email: str, password: str):
    # Проверяем, существует ли пользователь с таким email
    result = await db.execute(select(User).where(User.email == email))
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(status_code=400,
            detail="Пользователь с данных email адрессом уже зарегестрирован!")

    # Хэшируем пароль
    hashed_password = hash_password(password)

    # Создаем нового пользователя
    new_user = User(
        email=email,
        hashed_password=hashed_password
    )

    # Добавляем в БД
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user