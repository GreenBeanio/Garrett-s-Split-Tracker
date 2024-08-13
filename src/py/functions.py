# My imports
from py.classes import *

# Package Imports
import datetime
import zoneinfo
import hashlib
from flask import Flask


# Test to generate auth
def generateAuth(user: str, passw: str, age_s: int, sessions: dict) -> str:
    # Creating the expiration date
    exp = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        seconds=age_s
    )
    # Get a string of the current date time
    auth_s = str(exp) + user + passw
    auth_h = hashlib.sha256(auth_s.encode("utf-8")).hexdigest()
    # Saving the auth
    auth = UserAuth(user, auth_h, exp)
    # In production I would add this to a database, technically I don't even need to add the user in the class because it's stored as the key
    # Although it'd like to actually be able to have multiple sessions possibly. For if using on two devices. I suppose I could
    # grab the session id from the database instead too.
    sessions.update({user: auth})
    # Returning the auth for a cookie
    return auth_h


# Test to check authentication
def checkAuth(user: str, auth: str, sessions: dict) -> bool:
    # Check all sessions to see if a user has a session
    for s_user, s_auth in sessions.items():
        # Checking this because I'd like to have multiple sessions per user in the future ... maybe
        if s_user == user:
            # From the session object check the auth cookie
            if s_auth.auth == auth:
                # Check if the session has expired or not
                ct = datetime.datetime.now(datetime.timezone.utc)
                if s_auth.exp >= ct:
                    return True
                # If it isn't then delete the session
                else:
                    del sessions[s_user]
    return False


# Test to check users
def checkUser(username: str, password: str, users: list):
    for user in users:
        if user.username == username and user.password == password:
            return user
    return None
