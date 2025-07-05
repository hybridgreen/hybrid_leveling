
import datetime

class activity(BaseModel):
    id : int # Activity ID
    #date: datetime.date #Date and time of activity
    type: str #Run / Bike / Swim / Gym
    duration: int #Time in minutes

@app.post("activities/{id}")
def create_activity(type: str, duration: int):
    activity (
        id = 1,
        type = type,
        duration = duration
    )
    pass
