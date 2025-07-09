
from pydantic import BaseModel
from Activities import Activity
import database

class User(BaseModel):
    id: str # User ID
    name: str # username
    activities: dict[str,Activity]

def create_user(id: str , name : str):
    user_obj = User (
        id = id,
        name = name,
        activities= dict()
        )
    database.user_base[id] = user_obj

def fetch_user():
    id = ''
    while(id == ''):
        id = input("Enter your user id:")
        if id in database.user_base:
            user = database.user_base[id]
            print(f"Welcome {user.name}")
            return user
        print("User ID not recognised", end=None)
        id = ''