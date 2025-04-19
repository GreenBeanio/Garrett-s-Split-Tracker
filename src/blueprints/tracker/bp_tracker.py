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

# Import Credentials
from stored_credentials import app_config

# My Imports
from blueprints.auth.py.fn_getUserAuthProperBothName import getUserAuthProperBothName

# Package Imports
from flask import Blueprint, request, redirect, url_for, render_template
from typing import Union

# Create the blueprint
tracker_bp = Blueprint(
    "tracker", # Set the name to call from Flask
    __name__, # Set the module name for local flask resources or something like that
    template_folder="templates", # This uses a templates folder in the same directory as the module
    static_folder="static", # Separate static folder for the blueprint
    static_url_path="/static/tracker", # Set the url path for the static files
    url_prefix="/tracker", # Set the URL prefix
    # subdomain="auth", # Don't believe I want a subdomain
)

# Tests the path
#print(tracker_bp.root_path)

# Creating the specific tracked activity page
@tracker_bp.route("/user/<string:username>/activities")
def showTrackedActivities(username: str) -> Union[redirect, render_template]:
    """
    API ROUTE
    /user/<string:username>/activities
    
    GET API
    Show a User their page of tracked activities

    :param username: The username to show
    :type username: str
    """
    # Get information about if the user is logged in and is querying the right user
    auth_status, proper_status, c_user = getUserAuthProperBothName(
        request, app_config, username
    )
    # If the user is logged in and is checking themselves
    if proper_status:
        return render_template("tracked.j2", logged_in=auth_status, user=username)
    # If they are a logged in and searching the wrong account reroute them to their main account page (can't trust that the user has the same activities)
    elif auth_status:
        return render_template("tracker.j2", logged_in=auth_status, user=c_user)
    # If neither reroute them to the login page
    else:
        # Remove any existing cookies
        user_redirect = redirect(url_for("auth.showLogin"))
        user_redirect.delete_cookie("user")
        user_redirect.delete_cookie("auth")
        return user_redirect

# Creating the tracker page
@tracker_bp.get("/user/<string:username>")
def showTracker(username: str) -> Union[render_template, redirect]:
    """
    API ROUTE
    /user/<string:username>
    
    GET API
    Show a User their tracker page

    :param username: The username to show
    :type username: str
    """
    # Get information about if the user is logged in and is querying the right user
    auth_status, proper_status, c_user = getUserAuthProperBothName(
        request, app_config, username
    )
    # If the user is logged in and is checking themselves
    if proper_status:
        return render_template("tracker.j2", logged_in=auth_status, user=username)
    # If they are a logged in and searching the wrong account reroute them to their account (Naughty! Naughty!)
    elif auth_status:
        return render_template("tracker.j2", logged_in=auth_status, user=c_user)
    # If neither reroute them to the login page
    else:
        # Remove any existing cookies
        user_redirect = redirect(url_for("auth.showLogin"))
        user_redirect.delete_cookie("user")
        user_redirect.delete_cookie("auth")
        return user_redirect

# Footer Comment
# History of Contributions:
# [2024-2024] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]
