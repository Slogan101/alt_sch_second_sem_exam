from fastapi import APIRouter, status, HTTPException
from schemas.borrow_record import BorrowCreate
from services.borrow_record import borrow_crud

borrow_router = APIRouter()



@borrow_router.post("/", status_code=status.HTTP_201_CREATED)
def borrow_book(data: BorrowCreate):
    borrowed_book = borrow_crud.borrow_book(user_id=data.user_id, book_id=data.book_id, data=data)
    print(data)
    return borrowed_book

@borrow_router.get("/", status_code=status.HTTP_200_OK)
def get_borrow_records():
    records = borrow_crud.get_borrow_records()
    if not records:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No borrow record found.")
    return records

@borrow_router.get("/users/{user_id}", status_code=status.HTTP_200_OK)
def get_borrow_record(user_id: int):
    user_record = borrow_crud.get_user_record(user_id)
    return user_record

@borrow_router.put("/{id}/return", status_code=status.HTTP_200_OK)
def return_book(data: BorrowCreate):
    returned_book = borrow_crud.return_book(user_id=data.user_id, book_id=data.book_id)
    return returned_book