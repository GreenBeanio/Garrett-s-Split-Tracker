# Header Comment
# Project: [Garrett's Split Tracker] [https://github.com/GreenBeanio/Garrett-s-Split-Tracker]
# Copyright: Copyright (c) [2024]-[2025] [Garrett's Split Tracker] Contributors
# Version: [0.1]
# Status: [Development]
# License: [MIT]
# Author(s): [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Maintainer: [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Project Description: [This project is used to track "splits" in games or activities. With the ability to display them on a livestream.]
# File Description: [Creates the Flask App]

# My Imports
from classes.cl_Config import Config
from functions.fn_celeryInitApp import celeryInitApp

# Package Imports
from flask import Flask

# Creating the flask app (factory no passing name)
def createFlaskApp(config: Config) -> Flask:
    """
    Creates a Flask App

    :param config: The config object with the credentials
    :type config: Config

    :return: A Flask object
    :rtype: Flask
    """
    # Load the config
    # Creating the flask app
    flask_app = Flask(__name__)
    flask_app.config.update(Testing=config.testing, SECRET_KEY=config.secret_key)
    # flask_app.config.update(SERVER_NAME="your_domain.com") # Not sure about this yet
    # Add the stuff for celery
    flask_app.config.from_mapping(CELERY=config.celery_dict)
    flask_app.config.from_prefixed_env()
    celeryInitApp(flask_app)
    # Create the dictionary to return
    return flask_app

# Footer Comment
# History of Contributions:
# [2024-2025] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]