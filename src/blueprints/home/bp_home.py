# Header Comment
# Project: [Garrett's Split Tracker] [https://github.com/GreenBeanio/Garrett-s-Split-Tracker]
# Copyright: Copyright (c) [2024]-[2024] [Garrett's Split Tracker] Contributors
# Version: [0.1]
# Status: [Development]
# License: [MIT]
# Author(s): [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Maintainer: [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Project Description: [This project is used to track "splits" in games or activities. With the ability to display them on a livestream.]
# File Description: [The file holding the routes for the home blueprint]

# Import Credentials
from stored_credentials import app_config

# My imports
from auth.functions.fn_getUserAuthCookiesStatus import getUserAuthCookiesStatus

# Package Imports
from flask import Blueprint, request, render_template

# Create the blueprint
home_bp = Blueprint(
    "home",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static/",
    url_prefix="/",
    # subdomain="",
)

# Creating the main index route (Don't know if I want to put this into a blueprint or just leave it here)
@home_bp.get("/")
def index() -> render_template:
    print("hi")
    """
    API ROUTE
    /
    
    GET API
    Shows the website's homepage
    """
    # Get information about if the user is logged in
    c_user, auth_status = getUserAuthCookiesStatus(request, app_config)
    # Returning the welcome page
    return render_template("home.j2", logged_in=auth_status, user=c_user)

# Footer Comment
# History of Contributions:
# [2024-2025] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]
