from typing import Union
#from fastapi import FastAPI
from pydantic import BaseModel

import sys, os, json
from nanoid import generate
from datetime import date

from Users import User
from Activities import *
import database

# app = FastAPI()

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
    username = input("Please enter user name:")
    id = "U"+generate("123456789", size=3)
    print(f"Welcome, your id is {id}, please save it")
    database.user_base[id] = Users.create_user(id, username)

    return database.user_base[id]

def fetch_user():
    id = ''
    while(id == ''):
        id = input("Enter your user id:")
        if id in database.user_base:
            user = database.user_base[id]
            print(f"Welcome {user.name}")
            return user
        id = ''

def display_activities(user: User):
    for id in user.activities:
        item = user.activities[id]
        print("===================================")
        print(f"||Date: {item.timestamp}        ")
        print(f"||Activity type: {item.type}   ")
        print(f"||Activity duration: {item.duration}")
        print("===================================")
    pass

def main():
    
    print("Starting App")
    load()
    new_user = ''
    while(new_user == ''):
        new_user = input("Are you a new user? (y/n)").lower().strip()
        if new_user == 'y':
            user = create_new_user()
        elif new_user =='n':
            user = fetch_user()
        else:
            new_user= ''
            print("Error only y/n allowed. Try again")

    while(1):

        cmd = input("Enter command:").lower().strip()

        match cmd:
            case "add workout":

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
                save()

            case "display":
                display_activities(user)

            case "delete activity":
                del user.activities[input("Enter activity ID")]
            case "exit":
                print("Exiting...")
                save()
                sys.exit(0)
            case _:
                print("Unknown command")

    pass


main()