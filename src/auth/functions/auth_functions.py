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
from stored_credentials import app_config as saved_config

# Package Imports
import datetime
import hashlib
import secrets
import string
from flask import Request
from typing import Tuple
from celery import shared_task


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


# Function to get user auth cookie information
def getUserAuthCookies(request: Request) -> Tuple[str, str]:
    c_user = request.cookies.get("user")
    c_auth = request.cookies.get("auth")
    return (c_user, c_auth)


# Function to get user auth cookie information and auth status
def getUserAuthCookiesStatus(request: Request, config: Config) -> Tuple[str, bool]:
    c_user = request.cookies.get("user")
    c_auth = request.cookies.get("auth")
    auth_status = checkAuth(c_user, c_auth, config)
    return (c_user, auth_status)


# Function to get auth status from request
def getUserAuthStatus(request: Request, config: Config) -> bool:
    c_user = request.cookies.get("user")
    c_auth = request.cookies.get("auth")
    auth_status = checkAuth(c_user, c_auth, config)
    return auth_status


# Repeated task to remove expired sessions (currently running once an hour, if they try to connect with an expired session before that it'll be removed anyway)
# (This function is comment hell as a warning)
@shared_task()  # (ignore_result=False)
def removeExpiredSessions() -> None:
    # Get the mongodb session
    mongo_db = saved_config.mongo_con.get_database("split_tracker").get_collection(
        "sessions"
    )
    # Check that there are sessions before committing
    # (I could also do "len(list(sessions)) > 0", but I think the mongo query is probably faster than the conversion)
    # (I could also query time in mongodb, but I'm doing it in python in case there's time wumbo jumbo differences between the two)
    session_count = mongo_db.count_documents({})
    if session_count > 0:
        # Get all the sessions
        sessions = mongo_db.find({})
        # Iterate over the sessions
        for session in sessions:
            # # Testing time zones
            # local_tz = (
            #     datetime.datetime.now().astimezone().tzinfo
            # )  # Gets the local time zone
            # now = datetime.datetime.now(
            #     local_tz
            # )  # Get the local time that's time zone aware
            # print(datetime.datetime.tzname(now))  # Gets the timezone from a datetime
            # print(
            #     now.astimezone(tz=datetime.timezone.utc)
            # )  # Converts the time zone (gives the correct adjusted datetime)
            # print(
            #     now.replace(tzinfo=datetime.timezone.utc)
            # )  # Replaces the time zone (doesn't adjust the datetime just replaces the offset from the time zone! Probably not what you want!)
            # Extract the time and change the timezone (using replace because they should've been saved in UTC)
            exp = session["exp"].replace(tzinfo=datetime.timezone.utc)
            # Get the current time
            now = datetime.datetime.now(datetime.datetime.now().astimezone().tzinfo)
            # # Testing the different time zones methods again
            # dif = now - exp  # Gives the time you'd expect between the two time zones
            # dif2 = (
            #     now.astimezone(tz=datetime.timezone.utc) - exp
            # )  # Gives the same time because the datetimes have been adjusted
            # dif3 = (
            #     now.replace(tzinfo=datetime.timezone.utc) - exp
            # )  # Gives the wrong timedelta because the timezone was replaced not adjusted
            # print(dif)
            # print(dif2)
            # print(dif3)
            # dt_plain = datetime.datetime.now() # date time that is naive and has no time zone
            # dt_utc = datetime.datetime.now(datetime.timezone.utc) # Time zone that has the time adjusted for the given timezone (it works!)
            # dt_local = datetime.datetime.now(
            #     datetime.datetime.now().astimezone().tzinfo
            # ) # Time zone with your local time and time zone
            # If the expiration time is smaller than the current time delete it
            if exp <= now:
                # Delete based on the session id because it's guaranteed to be the most unique (even though auth should be as well)
                mongo_db.delete_one({"_id": session["_id"]})
    # # Testing debug methods since print doesn't work with the beat task
    # # Testing method 1
    # from celery.utils.log import get_task_logger
    # logger = get_task_logger(__name__)
    # logger.info("Method 1")
    # logger.info(sessions)
    # import logging
    # # Testing method 2
    # logger2 = logging.getLogger()
    # logger2.info("Method 2")
    # logger2.info(sessions)
    # # Testing method 3
    # print("Method 3")
    # print(sessions)
    # # They all worked actually I was tripping. They just show up in the celery worker console and not through flask.
    # # Kind of annoying, but it is what it is


# # Check the celery task name
# print(removeExpiredSessions.name)


# Footer Comment
# History of Contributions:
# [2024-2024] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]
