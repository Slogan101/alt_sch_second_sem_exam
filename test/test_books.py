from fastapi.testclient import TestClient
from unittest.mock import patch
from ..main import app
from schemas.books import Book, BookCreate
from services.books import BookCrud
from fastapi import status


client = TestClient(app)




def test_get_books():
    mock_books = [
    Book(id=1, title="title 1", author="author 1", is_available=True)
]
    
    with patch("routers.books.book_crud", spec=BookCrud) as mock_book_crud:
        mock_book_crud.get_books.return_value = mock_books

        response = client.get("/books")
        assert response.status_code == status.HTTP_200_OK
        assert len(mock_books) == 1

def test_get_book_id():
    mock_books = Book(id=1, title="title 1", author="author 1", is_available=True)

    with patch("routers.books.book_crud", spec=BookCrud) as mock_book_crud:
        mock_book_crud.get_book.return_value = mock_books

        response = client.get("/books/1")
        assert response.status_code == status.HTTP_200_OK
        print(response.json())
        assert response.json()["title"] == "title 1"
        assert response.json()["author"] == "author 1"
        assert response.json()["is_available"] == True

def test_create_user():
    mock_books = [
    Book(id=1, title="title 1", author="author 1", is_available=True),
]
    user_data = {
        "title": "title 2",
        "author": "author 2",
        "is_available": True
    }
    expected_output = {
        "title": "title 2",
        "author": "author 2",
        "is_available": True,
        "id": len(mock_books)+1
    }

    mock_create_book = Book(id=len(mock_books)+1, **user_data)
    mock_books.append(mock_create_book)

    with patch("routers.books.book_crud", spec=BookCrud) as mock_book_crud:
        mock_book_crud.create_book.return_value = mock_create_book

        response = client.post("/books", json=user_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert len(mock_books) == 2
        assert response.json() == expected_output
        mock_book_crud.create_book.assert_called_once_with(BookCreate(**user_data))

def test_update_book():
    mock_books = [
         Book(id=1, title="title 1", author="author 1", is_available=True)
    ]

    user_data = {
        "title": "title of book",
        "author": "author 2",
        "is_available": True
    }
    expected_output = {
        "title": "title of book",
        "author": "author 2",
        "is_available": True,
        "id": 1
    }

    with patch("routers.books.book_crud", spec=BookCrud) as mock_book_crud:
        mock_book_crud.get_book.return_value = mock_books
        mock_book_crud.update_book.return_value = expected_output

        response = client.put("/books/1", json=user_data)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_output

