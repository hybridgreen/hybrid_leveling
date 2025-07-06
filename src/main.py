from typing import Union
#from fastapi import FastAPI
from pydantic import BaseModel

import sys, os, json
from nanoid import generate
from datetime import date

import Users, Activity
import database

# app = FastAPI()

def save():
    cwd = os.getcwd()
    print(cwd)
    for id in database.user_base:
        user = database.user_base[id]
        path = os.path.join(cwd,user.name)

        with open(path,'a') as file:
            user_json = user.model_dump_json()

            file.write(user_json)
        pass


def main():
    
    print("Starting App")
    username = input("Please enter user name:")
    id = "U"+generate("123456789", size=3)
    if(id not  in database.user_base):
        database.user_base[id] = Users.create_user(id, username)
    user = database.user_base[id]
    while(1):

        cmd = input("Enter command:")

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

                try:
                    item = Activity.create_activity(activity_type, activity_dur, activity_rpe, activity_day)
                except Exception as e:
                    print(e)

                user.activities[item.id]= item

            case "display":
                print(user.activities)
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