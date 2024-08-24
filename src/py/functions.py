# My imports
from py.classes import *

# Package Imports
import datetime
import hashlib
import random
import secrets
import string
import pymongo
import json
import os
import sys
import pathlib


# Test to generate auth
def generateAuth(username: str, users: dict, age_s: int, sessions: dict) -> str:
    # Creating the expiration date
    exp = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        seconds=age_s
    )
    # Get a string of the current date time
    auth = hashlib.sha256(
        (str(exp) + username + users[username].hash_pass).encode("utf-8")
    ).hexdigest()
    # Saving the auth
    # In production I would add this to a database, technically I don't even need to add the user in the class because it's stored as the key
    # Although it'd like to actually be able to have multiple sessions possibly. For if using on two devices. I suppose I could
    # grab the session id from the database instead too.
    sessions.update({username: UserAuth(username, auth, exp)})
    # Returning the auth for a cookie
    return auth


# Test to check authentication
def checkAuth(user: str, auth: str, sessions: dict) -> bool:
    # Check all sessions to see if a user has a session
    for s_user, s_auth in sessions.items():
        # Checking this because I'd like to have multiple sessions per user in the future ... maybe
        if s_user == user:
            # From the session object check the auth cookie
            if s_auth.auth == auth:
                # Check if the session has expired or not
                if s_auth.exp >= datetime.datetime.now(datetime.timezone.utc):
                    return True
                # If it isn't then delete the session
                else:
                    del sessions[s_user]
    return False


# Test to check if a user exists
def checkUser(username: str, users: dict) -> bool:
    # New check user test!!!

    # Check the dictionary key (username string) to see if it matches
    for user in users:
        # If the username matches
        if user == username:
            return True
    return False


# Test to check if a provided password matches that users HashPass
def checkHashPass(password: str, user: UserObj) -> bool:
    # Check if the provided password is correct
    n_hash = createHashPass(password, user.salt)
    if n_hash == user.hash_pass:
        return True
    return False


# Test if a user is logging in correctly
def checkLogin(username: str, password: str, users: dict) -> bool:
    # Check if the user exists
    if checkUser(username, users):
        # Check if the password is correct by checking the HashPass
        if checkHashPass(password, users[username]):
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
def createUser(username: str, password: str, salt: str, users: dict) -> None:
    # Create the HashPass
    new_user = UserObj(username, createHashPass(password, salt), salt)
    users[username] = new_user


# Function to load our credentials
def loadCredentials(running_path) -> Config:
    # Create the path to the settings (where the main script is running then getting the directory)
    script_path = pathlib.Path(running_path).resolve().parent.resolve()
    json_path = pathlib.Path.joinpath(script_path, "config.json")
    # Load the file if it exists
    if pathlib.Path.exists(json_path):
        with open(json_path, "r") as file:
            # Load the json
            json_obj = json.load(file)
            # Convert the json into a class (why not, probably better than a dictionary)
            config_class = Config(
                secret_key=json_obj["SECRET_KEY"],
                mongo_addr=json_obj["MONGO_ADDRESS"],
                user=json_obj["MONGO_USER"],
                passwd=json_obj["MONGO_PASS"],
                mongo_port=json_obj["MONGO_PORT"],
            )
            return config_class
    else:
        default_json = {
            "SECRET_KEY": "YOUR_SECRET_KEY",
            "MONGO_ADDRESS": "ADDRESS_TO_MONGO",
            "MONGO_USER": "YOUR_MONGO_USER",
            "MONGO_PASS": "YOUR_MONGO_PASSWORD",
            "MONGO_PORT": "MONGO_PORT",
        }
        with open(json_path, "w+") as file:
            json_obj = json.dumps(default_json, indent=4, sort_keys=False, default=str)
            file.write(json_obj)
        # Maybe not the bes idea, but it is what it is
        sys.exit("Fill in the config file")
    # Create the file if it doesn't
