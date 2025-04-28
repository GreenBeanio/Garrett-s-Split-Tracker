# Header Comment
# Project: [Garrett's Split Tracker] [https://github.com/GreenBeanio/Garrett-s-Split-Tracker]
# Copyright: Copyright (c) [2024]-[2025] [Garrett's Split Tracker] Contributors
# Version: [0.1]
# Status: [Development]
# License: [MIT]
# Author(s): [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Maintainer: [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Project Description: [This project is used to track "splits" in games or activities. With the ability to display them on a livestream.]
# File Description: [A file holding the classes used in the tracker module]

# My imports
from py.cl_Config import Config
from blueprints.auth.py.cl_UserObj import UserObj

# Package Imports
from flask import jsonify

# Function to get all of a users Games or other Options
def getUserGames(username: str, config: Config):
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
    # Query Mongo for the 
    mongo_db = config.mongo_con.get_database("split_tracker").get_collection("games")
    # user_games = mongo_db.find({"username": username})
    distinct = mongo_db.distinct("game", {"username": username})
    return jsonify(distinct)


# Footer Comment
# History of Contributions:
# [2024-2025] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]
