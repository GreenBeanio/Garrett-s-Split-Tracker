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
from classes.credentials import Config

# from functions.load_credentials import loadCredentials
from stored_credentials import app_config

# My blueprints
from auth.auth import auth_bp

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


# # Creating the flask app (factory)
# def createFlaskApp(name: __name__, config: Config) -> Flask:
#     # Load the config
#     # Creating the flask app
#     flask_app = Flask(name)
#     flask_app.config.update(Testing=config.testing, SECRET_KEY=config.secret_key)
#     # Add the stuff for celery
#     flask_app.config.from_mapping(CELERY=config.celery_dict)
#     flask_app.config.from_prefixed_env()
#     celeryInitApp(flask_app)
#     # Create the dictionary to return
#     return flask_app


# Creating the flask app (factory no passing name)
def createFlaskApp(config: Config) -> Flask:
    # Load the config
    # Creating the flask app
    flask_app = Flask(__name__)
    flask_app.config.update(Testing=config.testing, SECRET_KEY=config.secret_key)
    # Add the stuff for celery
    flask_app.config.from_mapping(CELERY=config.celery_dict)
    flask_app.config.from_prefixed_env()
    celeryInitApp(flask_app)
    # Create the dictionary to return
    return flask_app


# Add blueprints to the flask apt
def addBlueprints(app: Flask):
    flask_app.register_blueprint(auth_bp)
    return app


# Get the config
# app_config = loadCredentials(__file__)  # Using the location of this main file

# Create the apps
# flask_app = createFlaskApp(__name__, app_config)
flask_app = createFlaskApp(app_config)
# celery_app: Celery = flask_app.extensions["celery"]

# Add the blueprints
flask_app_blue = addBlueprints(flask_app)

# Show the map
print(flask_app_blue.url_map)

# Start the flask app
if __name__ == "__main__":
    flask_app_blue.run(host="0.0.0.0", port=5000, debug=True)

# Footer Comment
# History of Contributions:
# [2024-2024] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]

# Test out a celery task
# @shared_task(ignore_reslt=False)
# def checkSessions(x) -> string:
#     return x


# result = checkSessions.delay("hi")
# result_result = AsyncResult(result.id)
# print(result_result.ready())
# print(result_result.successful())
# print(result_result.result)
