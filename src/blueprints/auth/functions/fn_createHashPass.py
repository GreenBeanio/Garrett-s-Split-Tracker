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
import hashlib

# Function to create a hashed password
def createHashPass(password: str, salt: str) -> str:
    """
    Hashes a password

    :param password: The password to hash
    :type password: str
    :param salt: The salt to hash the password with
    :type salt: str

    :return: The hashed password
    :rtype: str
    """
    hash_pass = hashlib.sha256((password + salt).encode("utf-8")).hexdigest()
    return hash_pass

# Footer Comment
# History of Contributions:
# [2024-2025] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]
