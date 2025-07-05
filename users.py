
from pydantic import BaseModel

class User(BaseModel):
    id: int # User ID
    name: str # username

def create_user(id: int , name : str):
    user_obj = User (
        id = id,
        name = name
        )
    return user_obj