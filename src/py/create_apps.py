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

# My imports
from py.functions import loadCredentials
from py.classes import Config

# Package Imports
from flask import Flask
from celery import Celery
from celery import Task


# Creating the celery app (Straight from the Flask documentation, I don't understand celery yet)
def celeryInitApp(flask_app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with flask_app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(flask_app.name, task_cls=FlaskTask)
    celery_app.config_from_object(flask_app.config["CELERY"])
    celery_app.set_default()
    flask_app.extensions["celery"] = celery_app
    return celery_app


# Creating the flask app
def createFlaskApp(file: __file__, name: __name__) -> dict[Flask, Celery, Config]:
    # Load the config
    app_config = loadCredentials(file)  # Using the location of this main file
    # Creating the flask app
    flask_app = Flask(__name__)
    flask_app.testing = True
    flask_app.secret_key = app_config.secret_key
    # Add the stuff for celery
    flask_app.config.from_mapping(CELERY=app_config.celery_dict)
    celery_app = celeryInitApp(flask_app)
    # Create the dictionary to return
    return {"Flask": flask_app, "Celery": celery_app, "Config": app_config}


# Footer Comment
# History of Contributions:
# [2024-2024] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]
