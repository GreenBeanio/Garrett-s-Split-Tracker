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
import secrets
import string

# Function to create a salt for a user
def createSalt() -> str:
    """
    Creates a salt

    :return: A new salt
    :rtype: str
    """
    # Generate a random string for the salt
    salt = "".join(
        secrets.choice(string.ascii_letters + string.digits + string.punctuation)
        for x in range(secrets.choice(range(5, 20)))
    )
    return salt

# Footer Comment
# History of Contributions:
# [2024-2025] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]
