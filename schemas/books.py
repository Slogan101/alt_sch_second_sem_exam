from pydantic import BaseModel
from typing import Optional


class BookBase(BaseModel):
    title: str
    author: str
    is_available: bool =True

class Book(BookBase):
    id: int

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    title: Optional[str] = None
    author: Optional[str] = None

class BookStatus(BaseModel):
    is_available: Optional[bool] = None