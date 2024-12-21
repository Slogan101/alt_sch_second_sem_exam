from schemas.books import Book, BookCreate, BookStatus, BookUpdate
from fastapi import HTTPException, status


books = [
    Book(id=1, title="Book 1", author="author 1", is_available=True),
    Book(id=2, title="Book 2", author="author 2", is_available=False),
    Book(id=3, title="Book 3", author="author 3", is_available=True),
]


class BookCrud:
    @staticmethod
    def get_books():
        return books
    
    @staticmethod
    def get_book(id):
        book = next((book for book in books if book.id == id), None)
        if not book:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Book not found or Unavailable.")
        return book
    
    @staticmethod
    def create_book(book: BookCreate):
        new_book = Book(id=len(book_crud.get_books())+1, **book.model_dump())
        books.append(new_book)
        return {"Book succesfully created": new_book}
    
    @staticmethod
    def update_book(book: Book, data: BookCreate):
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details="Book not found!")
        book.author = data.author
        book.title = data.title
        book.is_available = data.is_available
        return book
    
    @staticmethod
    def part_update(book: Book, data: BookUpdate):
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found!")
        if book:
            update_data = data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(book, key, value)
            return book
        
    @staticmethod
    def update_availability(book: Book, data: BookStatus):
        book.is_available = data.is_available
        return {"Status Updated Successfully": book}
        
    @staticmethod
    def delete_book(id):
        book = book_crud.get_book(id)
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found!")
        books.remove(book)
        return {"message": "Book deleted!"}


    




book_crud = BookCrud()