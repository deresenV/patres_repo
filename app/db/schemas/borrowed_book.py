from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BorrowedBookBase(BaseModel):
    book_id: int
    reader_id: int

class BorrowedBookCreate(BorrowedBookBase):
    pass

class BorrowedBookReturn(BaseModel):
    return_date: datetime

class BorrowedBookResponse(BorrowedBookBase):
    id: int
    borrow_date: datetime
    return_date: Optional[datetime] = None
    class Config:
        from_attributes = True 