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
from py.cl_Config import Config
from py.fn_celeryInitApp import celeryInitApp

# Package Imports
from flask import Flask

# Creating the flask app (factory no passing name)
def createFlaskApp(config: Config, ) -> Flask:
    """
    Creates a Flask App

    :param config: The config object with the credentials
    :type config: Config

    :return: A Flask object
    :rtype: Flask
    """
    # Load the config
    # Creating the flask app
    # Change templates if it's not main
    if __name__ == "__main__":
        flask_app = Flask(__name__)
    else:
        flask_app = Flask(__name__, template_folder="../templates", static_folder="../static")
        # import os
        # # Get the file path of the file
        # file_path = os.path.abspath(__file__)
        # # Go back 2 levels
        # file_path = os.path.dirname(os.path.dirname(file_path))
        # # This will look 2 directories back (parent), which will be the root folder in this project
        # # online says that I should be able to do "../templates", but it isn't working
        # flask_app.config.update(template_folder=os.path.join(file_path, "templates"),
        #                         static_folder=os.path.join(file_path, "static"))
        # # Well turns out that does work, but it wasnt' working because I was trying to use
        # # flask_app.config.update instead of setting it when making it... so yeah
        # flask_app = Flask(__name__, template_folder="../templates", static_folder="../static")
        # # Actually this works below by just setting it manually, but whatever... I'll just do it the way at the top
        # flask_app.template_folder = file_path
        # # print(flask_app.template_folder)
        # # print(flask_app.static_folder)
    # Update settings for the config
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