
from pydantic import BaseModel
from Activities import Activity

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
    return user_obj