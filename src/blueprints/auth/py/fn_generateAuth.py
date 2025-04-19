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
from py.cl_Config import Config
from blueprints.auth.py.fn_getUser import getUser

# Package Imports
import datetime
import hashlib

# Test to generate auth
def generateAuth(username: str, age_s: int, ip: str, config: Config) -> str:
    """
    Generates an Authentication Session for a Use (in MongoDB)

    :param username: The username to create the session for
    :type username: str
    :param age_s: Seconds until expiration of the session
    :type age_s: int
    :param ip: The ip of the connecting user [Check this later. I believe I made this to not let a session be used at a different ip.]
    :type ip: str
    :param config: The config object with the credentials
    :type config: Config

    :return: The session id
    :rtype: str
    """
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
    # Saving the auth
    mongo_db = config.mongo_con.get_database("split_tracker").get_collection("sessions")
    mongo_db.insert_one({"username": username, "auth": auth, "ip": ip, "exp": exp})
    # Returning the auth for a cookie
    return auth

# Footer Comment
# History of Contributions:
# [2024-2025] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]
