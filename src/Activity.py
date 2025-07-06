from nanoid import generate
from pydantic import BaseModel
import database
from datetime import date

class Activity(BaseModel):
    id : str # Activity ID
    timestamp: date #Date and time of activity
    type: str #Run / Bike / Swim / Gym
    duration: int #Time in minutes
    rpe: int 

#@app.post("activities/create")
def create_activity(type: str, duration: int, rpe: int, timestamp: date):
    activity = Activity (
        id = generate(size = 10),
        timestamp = timestamp,
        type = type,
        duration = duration,
        rpe = rpe
        )
    return activity

def display_activity(id):
    pass

def update_activity(id):
    pass

def delete_activity(id):
    pass

