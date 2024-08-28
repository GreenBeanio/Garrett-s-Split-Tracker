# Header Comment
# Project: [Garrett's Split Tracker] [https://github.com/GreenBeanio/Garrett-s-Split-Tracker]
# Copyright: Copyright (c) [2024]-[2024] [Garrett's Split Tracker] Contributors
# Version: [0.1]
# Status: [Development]
# License: [MIT]
# Author(s): [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Maintainer: [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Project Description: [This project is used to track "splits" in games or activities. With the ability to display them on a livestream.]
# File Description: [A file holding many functions used in the application.]

# My imports
from classes.credentials import Config
from auth.classes.auth_classes import UserObj
from auth.classes.auth_classes import UserAuth

# Package Imports
from pymongo import MongoClient
import datetime
import hashlib
import secrets
import string
import json
import sys
import pathlib


# Test to generate auth
def generateAuth(username: str, age_s: int, config: Config) -> str:
    # Get the user information
    user_info = getUser(username, config)
    # Creating the expiration date
    exp = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        seconds=age_s
    )
    # Get a string of the current date time (should I really include the password for this ... probably not, but it is a hash ...)
    auth = hashlib.sha256(
        (str(exp) + username + user_info.hash_pass).encode("utf-8")
    ).hexdigest()
    # NEW_HERE: Saving the auth!!!
    mongo_db = config.mongo_con.get_database("split_tracker").get_collection("sessions")
    mongo_db.insert_one({"username": username, "auth": auth, "exp": exp})
    # Returning the auth for a cookie
    return auth


# Test to check authentication
def checkAuth(user: str, auth: str, config: Config) -> bool:
    # NEW_HERE: Getting the sessions from mongo!!!
    mongo_db = config.mongo_con.get_database("split_tracker").get_collection("sessions")
    # Check if there is a session
    user_session = mongo_db.find_one({"username": user, "auth": auth})
    # Check if there was a valid result
    if user_session is None:
        return False
    else:
        # Make the datetime timezone aware
        user_dt = user_session["exp"].replace(tzinfo=datetime.timezone.utc)
        # Turn it into a class (I want to)
        user_s = UserAuth(user=user, auth=auth, exp=user_dt)
        # Check if the session hasn't expired
        if user_s.exp >= datetime.datetime.now(datetime.timezone.utc):
            print("Good session")
            return True
        # If it has expired then delete the session
        else:
            print("removing!!!")
            removeSession(user, auth, config)
        return False


# Test to check if a user exists
def checkUser(username: str, config: Config) -> bool:
    # Query Mongo
    mongo_db = config.mongo_con.get_database("split_tracker").get_collection("users")
    result = mongo_db.find_one({"username": username})
    # Check if there was a valid result (for a find_one, find is different)
    if result is None:
        return False
    else:
        return True


# Returns information about the user
def getUser(username: str, config: Config) -> UserObj:
    # Query Mongo
    mongo_db = config.mongo_con.get_database("split_tracker").get_collection("users")
    result = mongo_db.find_one({"username": username})
    # Create UserObj from the response (because I want to)
    user_obj = UserObj(
        username=result["username"], hash_pass=result["hash_pass"], salt=result["salt"]
    )
    return user_obj


# Removes a sessions (really probably only need the auth, but just to be sure I'll pass the username as well)
def removeSession(username: str, auth: str, config: Config):
    # Query Mongo
    mongo_db = config.mongo_con.get_database("split_tracker").get_collection("sessions")
    mongo_db.delete_one({"username": username, "auth": auth})


# Test to check if a provided password matches that users HashPass
def checkHashPass(password: str, user: UserObj) -> bool:
    # Check if the provided password is correct
    n_hash = createHashPass(password, user.salt)
    if n_hash == user.hash_pass:
        return True
    return False


# Test if a user is logging in correctly
def checkLogin(username: str, password: str, config: Config) -> bool:
    # Check if the user exists
    if checkUser(username, config):
        # Get the user information
        user_info = getUser(username, config)
        # Check if the password is correct by checking the HashPass
        if checkHashPass(password, user_info):
            return True
    return False


# Function to create a salt for a user
def createSalt() -> str:
    # Generate a random string for the salt
    salt = "".join(
        secrets.choice(string.ascii_letters + string.digits + string.punctuation)
        for x in range(secrets.choice(range(5, 20)))
    )
    return salt


# Function to create a hashed password
def createHashPass(password: str, salt: str) -> str:
    hash_pass = hashlib.sha256((password + salt).encode("utf-8")).hexdigest()
    return hash_pass


# Function to create a new user (Doing this for later)
def createUser(username: str, password: str, salt: str, config: Config) -> None:
    # NEW_HERE: Saving the new user!!!
    mongo_db = config.mongo_con.get_database("split_tracker").get_collection("users")
    mongo_db.insert_one(
        {
            "username": username,
            "hash_pass": createHashPass(password, salt),
            "salt": salt,
        }
    )


# Function to load our credentials
def loadCredentials(running_path: pathlib.Path) -> Config:
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
