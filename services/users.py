from schemas.users import User, UserCreate, UserStatus, UserUpdate
from fastapi import HTTPException, status





users = [
    User(id=1, name="User 1", email="email 1", is_active=True),
    User(id=2, name="User 2", email="email 2", is_active=False),
    User(id=3, name="User 3", email="email 3", is_active=True), 
]


class UserCrud:
    @staticmethod
    def get_users():
        return users
    

    @staticmethod
    def get_user(id):
        user = next((user for user in users if user.id == id), None)
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found.")
        return user
    
    @staticmethod
    def create_user(user: UserCreate):
        new_user = User(id=len(user_crud.get_users()) + 1, **user.model_dump())
        users.append(new_user)
        return new_user
    
    @staticmethod
    def update_user(user: User, data: UserCreate):
        user.name = data.name
        user.email = data.email
        return user
    
    @staticmethod
    def part_update_user(user: User, data: UserUpdate):
        update_data = data.model_dump(exclude_unset=True).items()
        for key, value in update_data:
            setattr(user, key, value)
        return user
    
    @staticmethod
    def update_user_status(user: User, data: UserStatus):
        user.is_active = data.is_active
        return {"Status Updated Successfully": user}
        
    @staticmethod
    def delete_user(id):
        user = user_crud.get_user(id)
       
        users.remove(user)
        return {"message": "User deleted!"}














user_crud = UserCrud()