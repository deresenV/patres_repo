from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base


class Reader(Base):
    __tablename__ = "readers"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    #password - по тз не требуется

    # Смежная табличка для связи с книгами
    borrowed_books = relationship("BorrowedBook", back_populates="reader")

