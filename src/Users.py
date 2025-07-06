
from pydantic import BaseModel

class User(BaseModel):
    id: str # User ID
    name: str # username
    activities: dict

def create_user(id: str , name : str):
    user_obj = User (
        id = id,
        name = name,
        activities= dict()
        )
    return user_obj