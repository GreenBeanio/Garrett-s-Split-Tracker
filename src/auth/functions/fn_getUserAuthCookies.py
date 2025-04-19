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

# Package Imports
from flask import Request
from typing import Tuple

# Function to get user auth cookie information (The user and the auth, not the status)
def getUserAuthCookies(request: Request) -> Tuple[str, str]:
    """
    Get the Auth Cookies from a connection

    :param request: The Flask Request
    :type request: Request

    :return: [The Username, The Session]
    :rtype: Tuple[str, str]
    """
    c_user = request.cookies.get("user")
    c_auth = request.cookies.get("auth")
    return (c_user, c_auth)

# Footer Comment
# History of Contributions:
# [2024-2025] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]