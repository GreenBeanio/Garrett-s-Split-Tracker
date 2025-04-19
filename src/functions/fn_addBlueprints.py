# Header Comment
# Project: [Garrett's Split Tracker] [https://github.com/GreenBeanio/Garrett-s-Split-Tracker]
# Copyright: Copyright (c) [2024]-[2025] [Garrett's Split Tracker] Contributors
# Version: [0.1]
# Status: [Development]
# License: [MIT]
# Author(s): [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Maintainer: [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Project Description: [This project is used to track "splits" in games or activities. With the ability to display them on a livestream.]
# File Description: [Add blueprints to the Flask App]

# My blueprints
from auth.bp_auth import auth_bp
from tracker.bp_tracker import tracker_bp

# Package Imports
from flask import Flask

# Add blueprints to the flask apt
def addBlueprints(flask_app: Flask) -> Flask:
    """
    Add Blueprints to a Flask App

    :param flask_app: The Flask app
    :type flask_app: Flask

    :return: The Flask with Blueprints added
    :rtype: Flask

    You have to manually add all the blueprints to this function
    """
    flask_app.register_blueprint(auth_bp)
    flask_app.register_blueprint(tracker_bp)
    return flask_app

# Footer Comment
# History of Contributions:
# [2024-2025] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]