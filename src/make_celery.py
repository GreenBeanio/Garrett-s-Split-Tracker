# Header Comment
# Project: [Garrett's Split Tracker] [https://github.com/GreenBeanio/Garrett-s-Split-Tracker]
# Copyright: Copyright (c) [2024]-[2024] [Garrett's Split Tracker] Contributors
# Version: [0.1]
# Status: [Development]
# License: [MIT]
# Author(s): [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Maintainer: [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Project Description: [This project is used to track "splits" in games or activities. With the ability to display them on a livestream.]
# File Description: [Used to create celery workers]

# My imports
from main import createFlaskApp
from celery import Celery

# from functions.load_credentials import loadCredentials
from stored_credentials import app_config

# Make a celery worker
# app_config = loadCredentials(__file__)  # Using the location of this main file
flask_app = createFlaskApp(app_config)
celery_app: Celery = flask_app.extensions["celery"]

# Footer Comment
# History of Contributions:
# [2024-2024] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]
