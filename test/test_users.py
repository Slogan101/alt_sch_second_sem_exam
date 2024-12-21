from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app
from schemas.users import User, UserCreate
from services.users import UserCrud
from fastapi import status


client = TestClient(app)

mock_users = [
        User(id=1, name="User 1", email="email 1", is_active=True)
    ]
    

def test_get_users():

    with patch("routers.users.user_crud", spec=UserCrud) as mock_user_crud:
        mock_user_crud.get_users.return_value = mock_users

        response = client.get("/users")
        assert response.status_code == status.HTTP_200_OK
        assert len(mock_users) == 1

def test_get_user_by_id():

    with patch("routers.users.user_crud", spec=UserCrud) as mock_user_crud:
        mock_user_crud.get_user.return_value = mock_users

    response = client.get("users/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "User 1"
    assert response.json()["email"] == "email 1"
    assert response.json()["is_active"] == True

def test_create_user():

    user_data = {
        "name": "Newson",
        "email": "newbay@gmail.com",
        "is_active": True
    }
    expected_output = {
        "name": "Newson",
        "email": "newbay@gmail.com",
        "is_active": True,
        "id": len(mock_users) + 1
    }

    mock_create_user = User(id=len(mock_users)+1, **user_data)
    mock_users.append(mock_create_user)

    with patch("routers.users.user_crud", spec=UserCrud) as mock_user_crud:
        mock_user_crud.create_user.return_value = mock_create_user

        response = client.post("/users", json=user_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert len(mock_users) == 2
        assert response.json() == expected_output
        mock_user_crud.create_user.assert_called_once_with(UserCreate(**user_data))
    
def test_update_user():
    user_data = {
        "name": "slogan",
        "email": "newbay@gmail.com",
        "is_active": True
    }
    expected_output = {
        "name": "slogan",
        "email": "newbay@gmail.com",
        "is_active": True,
        "id": 1
    }


    with patch("routers.users.user_crud", spec=UserCrud) as mock_user_crud:
        mock_user_crud.update_user.return_value = expected_output

        response = client.put("/users/1", json=user_data)
        print(response.json())
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_output
    

    
def test_part_update():
    user_data = {
        "name": "Triplicate"
    }
    expected_output = {
        "name": "Triplicate",
        "email": "newbay@gmail.com",
        "is_active": True,
        "id": 1
    }


    with patch("routers.users.user_crud", spec=UserCrud) as mock_user_crud:
        mock_user_crud.part_update_user.return_value = expected_output

        response = client.patch("/users/1", json=user_data)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_output

def test_update_user_status():
    user_data = {
        "is_active": False
    }
    expected_output = {
        "Status Updated Successfully": {
            "name": "slogan",
            "email": "newbay@gmail.com",
            "is_active": False,
            "id": 1
        }
        
    }

    with patch("routers.users.user_crud", spec=UserCrud) as mock_user_crud:
        mock_user_crud.update_user_status.return_value = expected_output

        response = client.patch("/users/1/active", json=user_data)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_output


def test_delete_user():
    expected_response = {}

    with patch("routers.users.user_crud", spec=UserCrud) as mock_user_crud:
        mock_user_crud.delete_user.return_value = expected_response

        response = client.delete("/users/1")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.text == ""