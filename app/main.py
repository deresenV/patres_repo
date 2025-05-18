from fastapi import FastAPI

from app.db.database import engine, Base
from app.routers.auth import auth_router
from app.routers.books import router as books_router

app = FastAPI()

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Вызов функции при старте приложения
@app.on_event("startup")
async def startup():
    await create_tables()

app.include_router(auth_router)
app.include_router(books_router)