from sqlalchemy import Column, Integer, String, CheckConstraint
from sqlalchemy.orm import relationship
from app.db.database import Base

# ID (автоматически генерируемый)
# Название (строка, обязательное)
# Автор (строка, обязательное)
# Год публикации (число, необязательное)
# ISBN (строка, должен быть уникальным, необязательное)
# Количество экземпляров (число, по умолчанию 1, не может быть меньше 0)

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    author = Column(String, nullable=False, index=True)
    year = Column(Integer, nullable=True)
    isbn = Column(String, unique=True, nullable=True, index=True)
    copy_versions = Column(Integer, default=1, nullable=False)
    description = Column(String, nullable=True)

    #Смежная табличка для связи с читателями
    borrowed_books = relationship("BorrowedBook", back_populates="book")

    # Добавляем проверку, чтобы copies_available >= 0
    __table_args__ = (
        CheckConstraint('copy_versions >= 0', name='check_copy_versions_positive'),
    )
