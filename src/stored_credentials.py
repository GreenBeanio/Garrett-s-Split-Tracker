# Header Comment
# Project: [Garrett's Split Tracker] [https://github.com/GreenBeanio/Garrett-s-Split-Tracker]
# Copyright: Copyright (c) [2024]-[2024] [Garrett's Split Tracker] Contributors
# Version: [0.1]
# Status: [Development]
# License: [MIT]
# Author(s): [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Maintainer: [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Project Description: [This project is used to track "splits" in games or activities. With the ability to display them on a livestream.]
# File Description: [Stores the credentials for other modules to call on]

# My imports
from classes.credentials import Config
from functions.load_credentials import loadCredentials


# My hope is that by storing this file seperate I can use it to store this variable in memory and call it from other modules.
# I have no idea if it actually works that way or if it's just going to call the function every time. Hopefully it stores it in memory.

# Get the config
app_config = loadCredentials(__file__)  # Using the location of this main file

# Footer Comment
# History of Contributions:
# [2024-2024] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]
