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
from auth.functions.fn_checkAuth import checkAuth

# Package Imports
from flask import Request
from typing import Tuple

# Function to check if the have auth status AND it's the same user! (No shenanigans allowed!) (Returns both the proper and auth status)
def getUserAuthProperBoth(
    request: Request, config: Config, search_user: str
) -> Tuple[bool, bool]:
    """
    Get the Auth Cookies from a connection

    :param request: The Flask Request
    :type request: Request
    :param config: The config object with the credentials
    :type config: Config
    :param search_user: The user to search for
    :type search_user: str

    :return: [If the authorization was successful, If the user is searching for themselves]
    :rtype: Tuple[bool, bool]
    """
    c_user = request.cookies.get("user")
    c_auth = request.cookies.get("auth")
    auth_status = checkAuth(c_user, c_auth, request.remote_addr, config)
    if auth_status and c_user == search_user:
        return auth_status, True
    else:
        return auth_status, False

# Footer Comment
# History of Contributions:
# [2024-2025] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]