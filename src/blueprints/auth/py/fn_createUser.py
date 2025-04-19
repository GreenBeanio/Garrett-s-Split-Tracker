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
from blueprints.auth.py.fn_createHashPass import createHashPass

# Function to create a new user (Doing this for later)
def createUser(username: str, password: str, salt: str, config: Config) -> None:
    """
    Creates a new user (in MongoDB)

    :param username: The username to create
    :type username: str
    :param password: The password to hash
    :type password: str
    :param salt: The salt to use to hash the password
    :type salt: str

    :param config: The config object with the credentials
    :type config: Config

    :return: Nothing
    :rtype: None
    """
    # Saving the new user
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
# [2024-2025] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]
