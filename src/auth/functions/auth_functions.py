# Header Comment
# Project: [Garrett's Split Tracker] [https://github.com/GreenBeanio/Garrett-s-Split-Tracker]
# Copyright: Copyright (c) [2024]-[2024] [Garrett's Split Tracker] Contributors
# Version: [0.1]
# Status: [Development]
# License: [MIT]
# Author(s): [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Maintainer: [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Project Description: [This project is used to track "splits" in games or activities. With the ability to display them on a livestream.]
# File Description: [A file holding many functions used in the auth module.]

# My imports
from classes.credentials import Config
from auth.classes.auth_classes import UserObj
from auth.classes.auth_classes import UserAuth

# Package Imports
import datetime
import hashlib
import secrets
import string


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
            return True
        # If it has expired then delete the session
        else:
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


# Footer Comment
# History of Contributions:
# [2024-2024] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]
