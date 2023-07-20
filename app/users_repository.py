from attrs import define 
from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str
    full_name: str
    password: str
    id: int = 0




class UsersRepository:
    def __init__(self):
        self.users = [User(username = "nurmash", email = "nurmash@mail.com", full_name = "Nurmash Omarbek", password = "nurmash", id = 1)]

    def save(self, user: User):
        id = len(self.users) + 1
        user.id = id
        self.users.append(user)

    def getAll(self):
        print (self.users)
    
    def get_by_email(self, email):
        for user in self.users:
            if email == user.email:
                return user
        return None
    
    def get_by_username(self, username):
        for user in self.users:
            if username == user.username:
                return user
        return None
    


    def get_by_id(self, user_id):
        for user in self.users:
            if user.id == user_id:
                return user
        return None