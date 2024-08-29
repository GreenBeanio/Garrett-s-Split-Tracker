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
    celery_app.set_default()  # Oh my god all my trouble was because I missed this line when I copied it in :cry:
    flask_app.extensions["celery"] = celery_app
    return celery_app


# Creating the flask app (factory no passing name)
def createFlaskApp(config: Config) -> Flask:
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


# Add blueprints to the flask apt
def addBlueprints(app: Flask):
    flask_app.register_blueprint(auth_bp)
    return app


# Create the apps
flask_app = createFlaskApp(app_config)

# If we want to use the celery app directly it's here
# celery_app: Celery = flask_app.extensions["celery"]

# Test function
from auth.functions.auth_functions import removeExpiredSessions

removeExpiredSessions()

# Add the blueprints
flask_app_blue = addBlueprints(flask_app)

# Show the blueprint map
# print(flask_app_blue.url_map)

# Start the flask app
if __name__ == "__main__":
    flask_app_blue.run(host="0.0.0.0", port=5000, debug=True)

# Then un these cli commands (running flask first seems to matter, but the order of these 2 doesn't really,
# but I start the beat first because the worker needs it):
# "celery -A make_celery beat --loglevel INFO"
# "celery -A make_celery worker --loglevel INFO"


# Footer Comment
# History of Contributions:
# [2024-2024] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]
