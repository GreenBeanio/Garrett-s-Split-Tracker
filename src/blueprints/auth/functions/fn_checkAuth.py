# Header Comment
# Project: [Garrett's Split Tracker] [https://github.com/GreenBeanio/Garrett-s-Split-Tracker]
# Copyright: Copyright (c) [2024]-[2025] [Garrett's Split Tracker] Contributors
# Version: [0.1]
# Status: [Development]
# License: [MIT]
# Author(s): [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Maintainer: [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Project Description: [This project is used to track "splits" in games or activities. With the ability to display them on a livestream.]
# File Description: [A file holding many functions used in the auth module.]

# My imports
from classes.cl_Config import Config
from auth.classes.cl_UserAuth import UserAuth
from auth.functions.fn_removeSession import removeSession

# Package Imports
import datetime

# Test to check authentication
def checkAuth(user: str, auth: str, ip: str, config: Config) -> bool:
    """
    Check the authentication of a user

    :param user: The username to check for authentication
    :type user: str
    :param auth: The authentication to check for the use
    :type auth: str
    :param ip: The ip address to check
    :type ip: str
    :param config: The config object with the credentials
    :type config: Config

    :return: If the authentication is valid or not
    :rtype: bool
    """
    # Getting the sessions from mongo
    mongo_db = config.mongo_con.get_database("split_tracker").get_collection("sessions")
    # Check if there is a session
    user_session = mongo_db.find_one({"username": user, "auth": auth})
    # Check if there was a valid result
    if user_session is None:
        return False
    else:
        # Make the datetime timezone aware
        user_dt = user_session["exp"].replace(tzinfo=datetime.timezone.utc)
        # Turn it into a class (I want to no real reason to but I already made the class)
        user_s = UserAuth(user=user, auth=auth, ip=ip, exp=user_dt)
        # Check if the session hasn't expired
        if user_s.exp >= datetime.datetime.now(
            datetime.datetime.now().astimezone().tzinfo
        ):
            # Return true regardless of ip if the user chose to ignore it when logging in
            if user_session["ip"] == "ignore":
                return True
            # Check if the user is logging in with the same ip
            elif user_s.ip == user_session["ip"]:
                return True
            else:
                return False
        # If it has expired then delete the session (regardless of if the correct user is trying to log in)
        else:
            removeSession(user, auth, config)
        return False

# Footer Comment
# History of Contributions:
# [2024-2025] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]
