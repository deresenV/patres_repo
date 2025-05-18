
from pydantic import BaseModel, Field, validator
from typing import Optional


class BookBase(BaseModel):
    title: str
    author: str
    year: Optional[int] = None
    isbn: Optional[str] = None
    copy_versions: int = Field(default=1, ge=0)

    # Дополнительная валидация (необязательно, но полезно)
    @validator('copy_versions')
    def check_copies(cls, v):
        if v < 0:
            raise ValueError("Copies available must be >= 0")
        return v


class BookCreate(BookBase):
    pass  # Можно добавить дополнительные ограничения при создании, если нужно


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None
    isbn: Optional[str] = None
    copy_versions: Optional[int] = None


class BookResponse(BookBase):
    id: int

    class Config:
        from_attributes = True  # Поддержка работы с SQLAlchemy моделями


class Book(BookResponse):
    pass