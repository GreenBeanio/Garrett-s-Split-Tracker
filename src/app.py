# Header Comment
# Project: [Garrett's Split Tracker] [https://github.com/GreenBeanio/Garrett-s-Split-Tracker]
# Copyright: Copyright (c) [2024]-[2024] [Garrett's Split Tracker] Contributors
# Version: [0.1]
# Status: [Development]
# License: [MIT]
# Author(s): [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Maintainer: [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Project Description: [This project is used to track "splits" in games or activities. With the ability to display them on a livestream.]
# File Description: [Creates the flask and celery apps.]

# Import Credentials
from stored_credentials import app_config

# My imports
from py.fn_createFlaskApp import createFlaskApp
from py.fn_addBlueprints import addBlueprints

# Create the apps
flask_app = createFlaskApp(app_config)

# If we want to use the celery app directly it's here
# celery_app: Celery = flask_app.extensions["celery"]

# Add the blueprints
flask_app = addBlueprints(flask_app)

# Footer Comment
# History of Contributions:
# [2024-2024] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]
