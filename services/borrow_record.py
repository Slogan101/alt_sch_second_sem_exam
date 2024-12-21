from datetime import date
from schemas.borrow_record import Borrow, BorrowCreate
from fastapi import HTTPException, status
from services.users import users
from services.books import books

borrow_records_data = []
user_borrow_records = []



class BorrowCrud:
    @staticmethod
    def borrow_book(user_id: int, book_id: int, data: BorrowCreate):
        # checking if the user exists and is active.
        user = next((user for user in users if user.id == user_id), None)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is Inactive.")
        
        # Checking if the book exists and is available
        book = next((book for book in books if book.id == book_id and book.is_available), None)
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found or Unavailable.")
        
        # Checking if the user_id and book_id exists in the borrow_records_data
        existing_record = next((record for record in borrow_records_data if record.user_id == user_id and record.book_id == book_id), None)
        if existing_record:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already borrowed this book. Kindly return to borrow again.")
        
        # Create the borrow record
        new_record = Borrow(id=len(borrow_records_data)+1, borrowed_date = date.today(), **data.model_dump(exclude_none=True))
        borrow_records_data.append(new_record)
        user_borrow_records.append(new_record)

        # Updating books availabilty
        book.is_available = False
        return {"message": "Book borrowed successfully.", "record": new_record}
    

    @staticmethod
    def get_borrow_records():
        return borrow_records_data
    
    @staticmethod
    def get_user_record(user_id):
        records = [r for r in user_borrow_records if r.user_id == user_id]
        if not records:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found.")
        return records
        # record = next((r for r in borrow_records_data if r.user_id == user_id), None)
        # if not record:
        #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found.")
        # return record
    
    @staticmethod
    def return_book(user_id: int, book_id: int):
        # Find an active record
        record = next((r for r in borrow_records_data if r.user_id == user_id and r.book_id == book_id and not r.return_date), None)
        if not record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found or book already returned!")
        
        # borrow records for a specific user
        records = [r for r in user_borrow_records if r.user_id == user_id and r.book_id == book_id]

        # Update the record
        record.return_date = date.today()
        for r in records:
            r.return_date = date.today()

        # Update the book availabilty

        book = next((b for b in books if b.id == book_id), None)
        book.is_available = True
        
        borrow_records_data.remove(record)
        return {"message": "Book returned successfully", "record": record}









borrow_crud = BorrowCrud()