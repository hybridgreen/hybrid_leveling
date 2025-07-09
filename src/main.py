from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from nicegui import ui

import sys, os, json
from nanoid import generate
from datetime import date

from Users import *
from Activities import *
import database

app = FastAPI()
main_page = ui.column()
result = None

def on_submit (id, username):
    create_user(id,username)
    ui.notify("User created!")
    #save()
    main_page.clear()

def save():
    log_dir = os.path.abspath(os.getcwd())+"/log"
    for id in database.user_base:
        user = database.user_base[id]
        path = os.path.join(log_dir,user.id)

        with open(path,'r') as file:
            user_json = user.model_dump_json()
            file.write(user_json)
        pass

def load():
    log_dir = os.path.abspath(os.getcwd())+"/log"
    userfiles = os.listdir(log_dir)
    for record in userfiles:
        with open(os.path.join(log_dir,record), 'r') as file:
            user_json = file.read()
            user = User.model_validate_json(user_json)
            database.user_base[user.id] = user
    pass

def create_new_user():
    main_page.clear()
    with ui.card():
        id = "U"+generate("123456789", size=3)
        ui.label(f"Welcome, your id is {id}, please save it")
        username = ui.input(label="Enter user name").props('clearable')
        ui.button('Submit', on_click = lambda : on_submit(id,username.value))
    return

def add_workout():

    activity_type = input("Activity type:")
    activity_dur = input("Activity length:")
    activity_rpe = input("(Optional)Enter effort:")

    if(activity_rpe == ''):
        activity_rpe = 0
    activity_day = input("(Optional)Enter activity date in ISO format:")
    if(activity_day == ''):
        activity_day = date.today()
    else:
        try:
            activity_day = date.fromisoformat(activity_day)
        except Exception as e:
            print(e)
    item =  create_activity(activity_type, activity_dur, activity_rpe, activity_day)
    user.activities[item.id]= item
    #save()


def display_activities(user: User):
    for id in user.activities:
        item = user.activities[id]
        print("===================================")
        print(f"||Date: {item.timestamp}        ")
        print(f"||Activity type: {item.type}   ")
        print(f"||Activity duration: {item.duration}")
        print("===================================")
    pass

def dashboard():
    with main_page:
        ui.button(label = 'Add Workout', on_click = lambda: add_workout())
        ui.button(label = 'View Activities', on_click = lambda: display_activities() )
    pass

def main():
    
    print("Starting App")
    load()

    with main_page:
        ui.label("Are you a new user?")
        ui.button('YES', on_click = create_new_user)
        ui.button('NO', on_click = fetch_user)

    ui.run()


main()