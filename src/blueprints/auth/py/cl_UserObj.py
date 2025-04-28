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

# test class just to store users
class UserObj:
    """
    Class to store a User

    :param username: The username
    :type username: str
    :param hash_pass: The hashed password of the user
    :type hash_pass: str
    :param salt: The salt used to hash the password
    :type salt: str
    """
    def __init__(self, username: str, hash_pass: str, salt: str):
        self.username = username
        self.hash_pass = hash_pass
        self.salt = salt

# Footer Comment
# History of Contributions:
# [2024-2025] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]
