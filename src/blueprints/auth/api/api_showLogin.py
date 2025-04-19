# Header Comment
# Project: [Garrett's Split Tracker] [https://github.com/GreenBeanio/Garrett-s-Split-Tracker]
# Copyright: Copyright (c) [2024]-[2025] [Garrett's Split Tracker] Contributors
# Version: [0.1]
# Status: [Development]
# License: [MIT]
# Author(s): [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Maintainer: [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Project Description: [This project is used to track "splits" in games or activities. With the ability to display them on a livestream.]
# File Description: [The file holding the auth module blueprint]

# Import Credentials
from stored_credentials import app_config

# My Imports
from auth.bp_auth import auth_bp
from auth.functions.fn_getUserAuthStatus import getUserAuthStatus

# Package Imports
from flask import render_template, request, redirect, url_for, make_response, flash


# Creating an interactive login page
@auth_bp.get("/login")
def showLogin() -> redirect | make_response:
    """
    API ROUTE
    /login

    GET API
    Show the login page if not logged in.
    Show the index page if logged in.
    """
    # Get information about if the user is logged in
    auth_status = getUserAuthStatus(request, app_config)
    # If the user isn't already logged in
    if not auth_status:
        # Remove any existing cookies
        user_render = make_response(render_template("login.j2", logged_in=auth_status))
        user_render.delete_cookie("user")
        user_render.delete_cookie("auth")
        return user_render
    # If they are already logged in
    else:
        flash("You're already logged in")
        return redirect(url_for("index"))

# Footer Comment
# History of Contributions:
# [2024-2025] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]