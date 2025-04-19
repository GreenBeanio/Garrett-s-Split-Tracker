# Header Comment
# Project: [Garrett's Split Tracker] [https://github.com/GreenBeanio/Garrett-s-Split-Tracker]
# Copyright: Copyright (c) [2024]-[2025] [Garrett's Split Tracker] Contributors
# Version: [0.1]
# Status: [Development]
# License: [MIT]
# Author(s): [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Maintainer: [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Project Description: [This project is used to track "splits" in games or activities. With the ability to display them on a livestream.]
# File Description: [Initializes a Celery Object for Flask]

# Package Imports
from flask import Flask
from celery import Celery
from celery import Task

# Creating the celery app (Straight from the Flask documentation, I don't understand celery yet)
def celeryInitApp(flask_app: Flask) -> Celery:
    """
    Initialize Celery App
    
    :param flask_app: A Flask object
    :type flask_app: Flask

    :return: A Celery object for Flask
    :rtype: Celery
    """
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with flask_app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(flask_app.name, task_cls=FlaskTask)
    celery_app.config_from_object(flask_app.config["CELERY"])
    celery_app.set_default()  # Oh my god all my trouble was because I missed this line when I copied it in :cry:
    flask_app.extensions["celery"] = celery_app
    return celery_app


# Footer Comment
# History of Contributions:
# [2024-2025] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]