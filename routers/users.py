from fastapi import APIRouter, status
from schemas.users import UserCreate, UserStatus, UserUpdate
from services.users import user_crud


user_router = APIRouter()


@user_router.get("/")
def get_users():
    users = user_crud.get_users()
    return users

@user_router.get("/{id}", status_code=status.HTTP_200_OK)
def get_user(id: int):
    user = user_crud.get_user(id)
    return user

@user_router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate):
    new_user = user_crud.create_user(payload)
    return new_user

@user_router.put("/{id}", status_code=status.HTTP_200_OK)
def update_user(id: int, payload:UserCreate):
    user = user_crud.get_user(id)
    updated_user = user_crud.update_user(user=user, data=payload)
    return updated_user

@user_router.patch("/{id}", status_code=status.HTTP_200_OK)
def part_update_user(id: int, payload: UserUpdate):
    user = user_crud.get_user(id)
    part_updated_user = user_crud.part_update_user(user=user, data=payload)
    return part_updated_user

@user_router.patch("/{id}/active", status_code=status.HTTP_200_OK)
def update_user_status(id: int, stat: UserStatus):
    user = user_crud.get_user(id)
    stat_update = user_crud.update_user_status(user, data=stat)
    return stat_update

@user_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int):
    user_crud.delete_user(id)