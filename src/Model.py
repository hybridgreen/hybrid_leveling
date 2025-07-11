# -------------------#
# ------Imports -----#
# -------------------#
from pydantic import BaseModel
from nanoid import generate
from datetime import date
import os
from appglobal import context

# -------------------#
#  Data Models       #
# -------------------#

class Activity(BaseModel):
    id : str # Activity ID
    timestamp: date #Date and time of activity
    type: str #Run / Bike / Swim / Gym
    duration: int #Time in minutes
    rpe: int 

class User(BaseModel):
    id: str # User ID
    name: str # username
    activities: dict[str,Activity]

# -------------------#
#  User Management   #
# -------------------#

def create_user(id: str , name : str):
    user_obj = User (
        id = id,
        name = name,
        activities= dict()
        )
    AppContext.users[id] = user_obj
    return user_obj

def fetch_user():
    id = ''
    while(id == ''):
        id = input("Enter your user id:")
        if id in context.users:
            user = context.users[id]
            print(f"Welcome {user.name}")
            
        ui.notify("User ID not recognised")
        id = ''

# -------------------#
#  Activity handling #
# -------------------#

def create_activity(type: str, duration: int, rpe: int, timestamp: date):
    activity = Activity (
        id = generate(size = 10),
        timestamp = timestamp,
        type = type,
        duration = duration,
        rpe = rpe
        )
    current_user.activities[id] = activity

def display_activity(id):
    pass

def update_activity(id):
    pass

def delete_activity(id):
    pass


# -------------------#
#  File handling     #
# -------------------#

def save():
    log_dir = os.path.abspath(os.getcwd())+"/log"
    for id in context.users:
        user = context.users[id]
        path = os.path.join(log_dir,user.id)

        with open(path,'+') as file:
            user_json = user.model_dump_json()
            file.write(user_json)
        pass

def load():
    print("Loading user data")
    log_dir = os.path.abspath(os.getcwd())+"/log"
    save_files = os.listdir(log_dir)

    for file in save_files:
        path = os.path.join(log_dir,file)
        with open(path, 'r') as json_file:
            user_json = json_file.read()
            context.users[file]=User.model_validate_json(user_json)