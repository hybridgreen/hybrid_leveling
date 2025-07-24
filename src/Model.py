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
    context.users[id] = user_obj
    return user_obj

# -------------------#
#  Activity handling #
# -------------------#

def create_activity(type: str, duration: int, rpe: int, timestamp: date):
    activity_id = generate(size = 10)
    activity = Activity (
        id = activity_id,
        timestamp = timestamp,
        type = type,
        duration = duration,
        rpe = rpe
        )
    context.current_user.activities[activity_id] = activity

def edit_activity(type: str, duration: int, rpe: int, timestamp: date, id):
    activity = Activity (
        id = id,
        timestamp = timestamp,
        type = type,
        duration = duration,
        rpe = rpe
        )
    context.current_user.activities[id] = activity

def delete_activity(id):
    del context.current_user.activities[id]
    pass


# -------------------#
#  File handling     #
# -------------------#

def save():
    log_dir = os.path.abspath(os.getcwd())+"/log"
    for id in context.users:
        user = context.users[id]
        path = os.path.join(log_dir,user.id)

        with open(path,'w') as file:
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

# -------------------#
#   Plan Generator  #
# -------------------#

def generate_week(current_time, activity_count, spread,max_budget = 6, no_long=1, no_mod=0, no_hard=1, long_ratio=0.3, hard_day = 2, long_day = 6):

    workout_list = []
    number_easy = activity_count - no_long - no_mod - no_hard
    number_rest =  7 - number_easy
    max_easy_duration = 60
    min_easy_duration = 30
    max_long_run = 180

    total_easy_h = spread[0] * current_time
    total_mod_h = spread[1] * current_time
    total_hard_h = spread[2] * current_time

    long_minutes = total_easy_h * long_ratio * 60
    long_minutes = max(60, min(long_minutes,max_long_run))

    remaining_easy_hours = total_easy_h - int(long_minutes/60)

    for i in range(number_easy):
        easy_minutes = int((remaining_easy_hours / number_easy)*60)
        easy_minutes = max(min_easy_duration, min(easy_minutes,max_easy_duration))
        workout_list.append(('Easy', easy_minutes))

    if no_mod > 0:
        for i in range(no_mod):
            workout_list.append(('Steady', int(total_mod_h / no_mod * 60)))

    if no_hard > 0:
        for i in range(no_hard):
            workout_list.append(('Hard', int(total_hard_h / no_hard * 60)))
    
    if no_long > 0:
        workout_list.append(('Long', int(long_minutes)))

    for i in range(number_rest):
        workout_list.append(('Rest', 0))

    for index, workout in enumerate(workout_list):
        if 'Hard' == workout[0]:
            temp = workout_list[hard_day]
            workout_list[hard_day] = workout
            workout_list[index] = temp
        if 'Long' == workout[0]:
            temp = workout_list[long_day]
            workout_list[long_day] = workout
            workout_list[index] = temp
            
    total_training_time = 0


    for i in range(len(workout_list)):
        total_training_time += workout_list[i][1]
    
    if total_training_time > max_budget*60:
        return generate_week(max_budget, activity_count, spread, max_budget= max_budget)
    else:
        return workout_list
    

def generate_split(current_time, budget, number_of_runs, hard_day = 2, long_day = 6):  
    
    spread = (0.8, 0, 0.2) # Easy, Steady, Hard
    block = []

    week1 = generate_week(current_time, number_of_runs, spread, max_budget=budget, long_ratio= 0.3,hard_day = hard_day, long_day = long_day)
    block.append(week1)
    current_time *= 1.1

    week2 = generate_week(current_time, number_of_runs, spread, max_budget=budget, long_ratio= 0.4,hard_day = hard_day, long_day = long_day)
    block.append(week2)
    current_time *= 1.1

    week3 = generate_week(current_time, number_of_runs, spread, max_budget=budget, long_ratio= 0.5,hard_day = hard_day, long_day = long_day)
    block.append(week3)
    current_time *= 0.8

    week4 = generate_week(current_time, number_of_runs, spread, max_budget=budget, long_ratio= 0.3,hard_day = hard_day, long_day = long_day)
    block.append(week4)

    return block

