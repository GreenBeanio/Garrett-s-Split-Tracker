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
from blueprints.auth.py.cl_UserObj import UserObj

# Returns information about the user
def getUser(username: str, config: Config) -> UserObj:
    """
    Gets a User Object

    :param username: The username to get
    :type username: str
    :param config: The config object with the credentials
    :type config: Config

    :return: A User Object
    :rtype: UserObj
    """
    # Query Mongo
    mongo_db = config.mongo_con.get_database("split_tracker").get_collection("users")
    result = mongo_db.find_one({"username": username})
    # Create UserObj from the response (because I want to)
    user_obj = UserObj(
        username=result["username"], hash_pass=result["hash_pass"], salt=result["salt"]
    )
    return user_obj

# Footer Comment
# History of Contributions:
# [2024-2025] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]
