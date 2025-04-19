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

# Removes a sessions (really probably only need the auth, but just to be sure I'll pass the username as well)
def removeAllUserSessions(username: str, config: Config):
    """
    Removes all of a User's Sessions from MongoDB

    :param username: The username to remove the sessions for
    :type username: str
    :param config: The config object with the credentials
    :type config: Config

    :return: Nothing
    :rtype: None
    """
    # Query Mongo
    mongo_db = config.mongo_con.get_database("split_tracker").get_collection("sessions")
    mongo_db.delete_many({"username": username})

# Footer Comment
# History of Contributions:
# [2024-2025] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]
