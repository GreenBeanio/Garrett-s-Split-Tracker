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
from blueprints.auth.py.cl_UserObj import UserObj
from blueprints.auth.py.fn_createHashPass import createHashPass

# Test to check if a provided password matches that users HashPass
def checkHashPass(password: str, user: UserObj) -> bool:
    """
    Check the authentication of a user

    :param password: The password to check
    :type password: str
    :param user: The user to check the password of
    :type user: UserObj

    :return: If password passed matches the user
    :rtype: bool
    """
    # Check if the provided password is correct
    n_hash = createHashPass(password, user.salt)
    if n_hash == user.hash_pass:
        return True
    return False

# Footer Comment
# History of Contributions:
# [2024-2025] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]
