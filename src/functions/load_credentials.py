# Header Comment
# Project: [Garrett's Split Tracker] [https://github.com/GreenBeanio/Garrett-s-Split-Tracker]
# Copyright: Copyright (c) [2024]-[2024] [Garrett's Split Tracker] Contributors
# Version: [0.1]
# Status: [Development]
# License: [MIT]
# Author(s): [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Maintainer: [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Project Description: [This project is used to track "splits" in games or activities. With the ability to display them on a livestream.]
# File Description: [Loads the credentials]

# My Imports
from classes.credentials import Config

# My Imports for celery beats
# import auth.functions.auth_functions

# Imports
import json
import pathlib
import sys
from pymongo import MongoClient
import datetime


# Function to load our credentials
def loadCredentials(running_path: pathlib.Path) -> Config:
    # print("uh oh tried again!!!!!!")
    # Create the path to the settings (where the main script is running then getting the directory)
    script_path = pathlib.Path(running_path).resolve().parent.resolve()
    json_path = pathlib.Path.joinpath(script_path, "config.json")
    # Load the file if it exists
    if pathlib.Path.exists(json_path):
        with open(json_path, "r") as file:
            # Load the json
            json_obj = json.load(file)

        # Create a mongoDB connection
        mongo_client = MongoClient(
            f'mongodb://{json_obj["MONGO_USER"]}:{json_obj["MONGO_PASS"]}@{json_obj["MONGO_ADDRESS"]}:{json_obj["MONGO_PORT"]}/?authSource=split_tracker'
        )  # add ", tls=true" when that is set up

        # Create the celery dict
        celery_dict = dict(
            broker_url=f'redis://ANY_USERNAME:{json_obj["REDIS_PASS"]}@{json_obj["REDIS_ADDRESS"]}:{json_obj["REDIS_PORT"]}',
            result_backend=f'redis://ANY_USERNAME:{json_obj["REDIS_PASS"]}@{json_obj["REDIS_ADDRESS"]}:{json_obj["REDIS_PORT"]}',
            task_ignore_result=True,
            # Beat schedule for timing repetitive events (You can set up the schedules in here like this too instead of with the functions)
            # "task-name" : {"task": "function", "schedule": time_in_seconds}
            # beat_schedule={
            #     "task-every-minute": {
            #         "task": "auth.functions.auth_functions.removeExpiredSessions",
            #         "schedule": datetime.timedelta(seconds=1),
            #     }
            # },
        )

        # Convert the json into a class (why not, probably better than a dictionary)
        # Putting the mongodb connection in here may be very foolish. I might want to just connect multiple times.
        config_class = Config(
            # Secret key for flask
            secret_key=json_obj["SECRET_KEY"],
            testing=json_obj["TESTING"],
            # Mongo config
            mongo_addr=json_obj["MONGO_ADDRESS"],
            mongo_port=json_obj["MONGO_PORT"],
            mongo_user=json_obj["MONGO_USER"],
            mongo_passwd=json_obj["MONGO_PASS"],
            mongo_con=mongo_client,
            # Celery/Redis config
            redis_addr=json_obj["REDIS_ADDRESS"],
            redis_port=json_obj["REDIS_PORT"],
            redis_passwd=json_obj["REDIS_PASS"],
            celery_dict=celery_dict,
            # I don't even really need to store the password, address, and user name if I only make the connection here. We'll see if I change that later.
        )
        # print(auth.functions.auth_functions.removeExpiredSessions.name)  # TEMP: Checking celery
        return config_class
    # Create a file if it doesn't exist
    else:
        default_json = {
            "SECRET_KEY": "YOUR_SECRET_KEY",
            "TESTING": "TRUE_OR_FALSE",
            "MONGO_ADDRESS": "ADDRESS_TO_MONGO",
            "MONGO_PORT": "MONGO_PORT",
            "MONGO_USER": "YOUR_MONGO_USER",
            "MONGO_PASS": "YOUR_MONGO_PASSWORD",
            "REDIS_ADDRESS": "ADDRESS_TO_REDIS",
            "REDIS_PORT": "REDIS_PORT",
            "REDIS_PASS": "YOUR_REDIS_PASSWORD",
        }
        with open(json_path, "w+") as file:
            json_obj = json.dumps(default_json, indent=4, sort_keys=False, default=str)
            file.write(json_obj)
        # Maybe not the bes idea, but it is what it is
        sys.exit("Fill in the config file")


# Footer Comment
# History of Contributions:
# [2024-2024] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]
