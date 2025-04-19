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
from auth.functions.fn_checkUser import checkUser
from auth.functions.fn_createUser import createUser
from auth.functions.fn_createSalt import createSalt
from auth.functions.fn_generateAuth import generateAuth

# Package Imports
from flask import request, redirect, url_for, flash

# Handling attempts to create users very crudely
@auth_bp.post("/create-attempt")
def createAttempt() -> redirect:
    """
    API ROUTE
    /create-attempt
    
    POST API
    If successful shows the new users page
    If unsuccessful shows the website index page
    """
    user = request.form["user_box"]
    passw = request.form["pass_box"]
    # Check if the user doesn't already exist
    if not checkUser(user, app_config):
        # Generate a new user and their salt
        createUser(user, passw, createSalt(), app_config)
        # Generate auth for the new user
        age_s = 60 * 60  # 1 hour
        auth = generateAuth(
            user, age_s, request.remote_addr, app_config
        )  # Generate the new users auth with ip addr protection just in case
        # Generate cookie
        user_redirect = redirect(url_for("auth.showUser", username=user))
        user_redirect.set_cookie("user", user, max_age=age_s)
        user_redirect.set_cookie("auth", auth, max_age=age_s)
        return user_redirect
    else:
        flash("User already exists")
        return redirect(url_for("index"))

# Footer Comment
# History of Contributions:
# [2024-2025] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]