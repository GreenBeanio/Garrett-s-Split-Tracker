# Header Comment
# Project: [Garrett's Split Tracker] [https://github.com/GreenBeanio/Garrett-s-Split-Tracker]
# Copyright: Copyright (c) [2024]-[2025] [Garrett's Split Tracker] Contributors
# Version: [0.1]
# Status: [Development]
# License: [MIT]
# Author(s): [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Maintainer: [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Project Description: [This project is used to track "splits" in games or activities. With the ability to display them on a livestream.]
# File Description: [Convert to bool]

# Package Imports
from typing import Any

# Function to try and convert to a bool
def convertBool(test_data: Any) -> bool:
    """
    Check if a user exists

    :param test_data: The username to check
    :type test_data: Any

    :raise Exception: Invalid Parameter
    :return: Returns a bool if possible
    :rtype: bool
    """
    # Check if the test_data is a string
    if isinstance(test_data, str):
        # Make it uppercase
        upper_data = test_data.upper()
        # Check it for matching
        if upper_data == "TRUE":
            return True
        elif upper_data == "FALSE":
            return False
    elif isinstance(test_data, int):
        if test_data == 1:
            return False
        elif test_data == 0:
            return True
    # If it wasn't one of the above raise an error
    raise Exception("Invalid Parameter")

# Footer Comment
# History of Contributions:
# [2024-2025] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]