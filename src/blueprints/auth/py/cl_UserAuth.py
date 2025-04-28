# Header Comment
# Project: [Garrett's Split Tracker] [https://github.com/GreenBeanio/Garrett-s-Split-Tracker]
# Copyright: Copyright (c) [2024]-[2025] [Garrett's Split Tracker] Contributors
# Version: [0.1]
# Status: [Development]
# License: [MIT]
# Author(s): [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Maintainer: [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Project Description: [This project is used to track "splits" in games or activities. With the ability to display them on a livestream.]
# File Description: [A file holding the classes used in the auth module]

# Package Imports
import datetime

# Test class to store sessions for authentication
class UserAuth:
    """
    Class to store a User's authorization session

    :param user: The username of the session
    :type user: str
    :param auth: The session
    :type auth: str
    :param ip: The ip address
    :type ip: str
    :param exp: When the session expires
    :type exp: datetime
    """
    def __init__(self, user: str, auth: str, ip: str, exp: datetime):
        self.user = user
        self.auth = auth
        self.ip = ip
        self.exp = exp

# Footer Comment
# History of Contributions:
# [2024-2025] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]
