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
from main import app_config

# My Imports
from auth.bp_auth import auth_bp
from auth.functions.fn_getUserAuthStatus import getUserAuthStatus

# Package Imports
from flask import render_template, request, redirect, url_for, make_response, flash

# Creating an interactive account creations page
@auth_bp.get("/new-user")
def newUser() -> redirect | make_response:
    """
    API ROUTE
    /new-user
    
    GET API
    Shows the new user page
    """
    # Get information about if the user is logged in
    auth_status = getUserAuthStatus(request, app_config)
    if not auth_status:
        # Remove any existing cookies
        user_render = make_response(
            render_template("new_user.j2", logged_in=auth_status)
        )
        user_render.delete_cookie("user")
        user_render.delete_cookie("auth")
        return user_render
    else:
        flash("You're already logged in")
        return redirect(url_for("index"))

# Footer Comment
# History of Contributions:
# [2024-2025] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]