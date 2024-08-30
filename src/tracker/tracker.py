# Header Comment
# Project: [Garrett's Split Tracker] [https://github.com/GreenBeanio/Garrett-s-Split-Tracker]
# Copyright: Copyright (c) [2024]-[2024] [Garrett's Split Tracker] Contributors
# Version: [0.1]
# Status: [Development]
# License: [MIT]
# Author(s): [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Maintainer: [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Project Description: [This project is used to track "splits" in games or activities. With the ability to display them on a livestream.]
# File Description: [The file holding the tracking module blueprint]

# Import app config information
from stored_credentials import app_config

# My imports
from auth.functions.auth_functions import checkAuth
from auth.functions.auth_functions import checkLogin
from auth.functions.auth_functions import generateAuth
from auth.functions.auth_functions import removeSession
from auth.functions.auth_functions import removeAllUserSessions
from auth.functions.auth_functions import createSalt
from auth.functions.auth_functions import createUser
from auth.functions.auth_functions import checkUser
from auth.functions.auth_functions import getUserAuthCookies
from auth.functions.auth_functions import getUserAuthCookiesStatus
from auth.functions.auth_functions import getUserAuthStatus
from auth.functions.auth_functions import getUserAuthCookiesStatusFull

# New Imports
from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import make_response
from flask import url_for
from flask import flash
from markupsafe import escape

# Create the blueprint
tracker_bp = Blueprint(
    "tracker",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static/tracker",
    url_prefix="/tracker",
)


# Creating the tracker page
@tracker_bp.route("/<string:username>")
def showTracker(username):
    # Get information about if the user is logged in
    auth_status = getUserAuthStatus(request, app_config)
    # If the user isn't already logged in
    if auth_status:
        return render_template("tracker.j2", logged_in=auth_status, user=username)
    else:
        return "Naughty Naughty"
    # return f"User is {escape(username)}"


# Creating the specific tracked activity page
@tracker_bp.route("/<string:username>/<string:activity>")
def showTrackedActivity(username, activity):
    return f"User is {escape(username)} for the activity {escape(activity)}"


# Footer Comment
# History of Contributions:
# [2024-2024] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]
