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

# Test to check if a user exists
def checkUser(username: str, config: Config) -> bool:
    """
    Check if a user exists

    :param username: The username to check
    :type username: str
    :param config: The config object with the credentials
    :type config: Config

    :return: If username exists
    :rtype: bool
    """
    # Query Mongo
    mongo_db = config.mongo_con.get_database("split_tracker").get_collection("users")
    result = mongo_db.find_one({"username": username})
    # Check if there was a valid result (for a find_one, find is different)
    if result is None:
        return False
    else:
        return True

# Footer Comment
# History of Contributions:
# [2024-2025] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]
