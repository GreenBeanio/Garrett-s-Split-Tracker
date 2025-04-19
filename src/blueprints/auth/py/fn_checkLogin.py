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
from blueprints.auth.py.fn_checkUser import checkUser
from blueprints.auth.py.fn_getUser import getUser
from blueprints.auth.py.fn_checkHashPass import checkHashPass


# Test if a user is logging in correctly
def checkLogin(username: str, password: str, config: Config) -> bool:
    """
    Check the authentication of a user

    :param username: The username to check
    :type username: str
    :param password: The password to check
    :type password: str
    :param config: The config object with the credentials
    :type config: Config

    :return: If login is valid
    :rtype: bool
    """
    # Check if the user exists
    if checkUser(username, config):
        # Get the user information
        user_info = getUser(username, config)
        # Check if the password is correct by checking the HashPass
        if checkHashPass(password, user_info):
            return True
    return False

# Footer Comment
# History of Contributions:
# [2024-2025] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]
