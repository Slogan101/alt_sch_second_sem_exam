from pydantic import BaseModel
from typing import Optional
from datetime import date

class BorrowRecord(BaseModel):
    user_id: int
    book_id: int

class Borrow(BorrowRecord):
    id: int
    borrowed_date: date
    return_date: Optional[date] = None
    

class BorrowCreate(BorrowRecord):
    pass

