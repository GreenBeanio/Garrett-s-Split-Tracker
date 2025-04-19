# Header Comment
# Project: [Garrett's Split Tracker] [https://github.com/GreenBeanio/Garrett-s-Split-Tracker]
# Copyright: Copyright (c) [2024]-[2025] [Garrett's Split Tracker] Contributors
# Version: [0.1]
# Status: [Development]
# License: [MIT]
# Author(s): [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Maintainer: [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Project Description: [This project is used to track "splits" in games or activities. With the ability to display them on a livestream.]
# File Description: [Checks Paths]

# Package Imports
import pathlib
import logging

# Function to check if a path exists
def checkPath(
    path: pathlib.Path, has_error: bool, variable: str, log: logging.Logger
) -> bool:
    """
    Check if a path exists

    :param path: The path to check
    :type path: pathlib.Path
    :param has_error: A boolean for tracking errors
    :type has_error: bool
    :param variable: A string to print which path is missing
    :type variable: str
    :param log: The logger to use
    :type log: logging.Logger

    :return: If the path exists
    :rtype: bool
    """
    # If the path exists return a result based off the existing has_error
    if pathlib.Path.exists(path):
        return has_error
    # If the path doesn't exist return an error
    else:
        log.warning(f'Invalid path for "{variable}"')
        return True

# Footer Comment
# History of Contributions:
# [2024-2025] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]