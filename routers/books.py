from fastapi import APIRouter
from schemas.books import Book, BookCreate, BookStatus, BookUpdate
from  services.books import book_crud
from fastapi import status

book_router = APIRouter()


@book_router.get("/", status_code=status.HTTP_200_OK)
def get_books():
    books = book_crud.get_books()
    return books

@book_router.get("/{id}", status_code=status.HTTP_200_OK)
def get_book(id: int):
    book = book_crud.get_book(id)
    return book

@book_router.post("/", status_code=status.HTTP_201_CREATED)
def create_book(payload: BookCreate):
    book = book_crud.create_book(payload)
    return book

@book_router.put("/{id}", status_code=status.HTTP_200_OK)
def update_book(id: int, payload: BookCreate):
    book = book_crud.get_book(id)
    updated_book = book_crud.update_book(book=book, data=payload)
    return updated_book

@book_router.patch("/{id}")
def part_update(id: int, payload: BookUpdate):
    book = book_crud.get_book(id)
    part_updated = book_crud.part_update(book=book, data=payload)
    return part_updated

@book_router.patch("/{id}/availabilty", status_code=status.HTTP_200_OK)
def update_avilability(id: int, stat:BookStatus):
    book = book_crud.get_book(id)
    availability = book_crud.update_availability(book, stat)
    return availability



@book_router.delete("/{id}")
def delete_book(id: int):
    book_crud.delete_book(id)