# Header Comment
# Project: [Garrett's Split Tracker] [https://github.com/GreenBeanio/Garrett-s-Split-Tracker]
# Copyright: Copyright (c) [2024]-[2025] [Garrett's Split Tracker] Contributors
# Version: [0.1]
# Status: [Development]
# License: [MIT]
# Author(s): [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Maintainer: [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Project Description: [This project is used to track "splits" in games or activities. With the ability to display them on a livestream.]
# File Description: [Validate Config Data]

# Package Imports
import logging
import sys
from typing import Any, Type, Callable, Tuple

# Function to validate data type
def validateData(
    test_data: Any,
    desired_type: Type,
    conversion_fun: Callable[[Any], Any],
    parameter: str,
    logger: logging.Logger,
) -> Tuple[bool, Any]:
    """
    Check if a user exists

    :param test_data: Data to test
    :type test_data: Any
    :param desired_type: The type to check data against
    :type desired_type: Type
    :param conversion_fun: A function to try and convert the data
    :type conversion_fun: Callable[[Any], Any]
    :param parameter: A string to return if there's an error
    :type parameter: str
    :param logger: The logger to use
    :type logger: logging.Logger
    
    :return: [If the data is valid, the data]
    :rtype: Tuple[bool, Any]
    """
    # Check if it's the correct type, and it's not a string (because we have multiple string conversion types)
    if isinstance(test_data, desired_type) and not isinstance(test_data, str):
        return (True, test_data)
    # Try to to convert the data
    try:
        return (True, conversion_fun(test_data))
    except:
        logger.warning(
            f'Value for "{parameter}" is the incorrect type. It must be a/an {str(desired_type)}.'
        )
        return (False, test_data)

# Footer Comment
# History of Contributions:
# [2024-2025] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]