from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
import sys, os

import users

app = FastAPI()
user_base = []

def main():

    argv = sys.argv.copy()
    
    if(len(argv) < 2):
        print("Error: User not specified")
        sys.exit(1)
    
    user_base.append(users.create_user(1, argv[1]))
    print(user_base)
    pass


main()