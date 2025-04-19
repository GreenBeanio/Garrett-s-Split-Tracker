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
from auth.functions.fn_getUserAuthProperBothName import getUserAuthProperBothName

# Package Imports
from flask import render_template, request, redirect, url_for

###
# Note: huge problem is that right now seemingly if you authenticate a session for any user it'll let you go to any users page!
# Just have it check you're going to your page or not. Something like that
###

# Creating the user page
@auth_bp.get("/user/<string:username>")
def showUser(username: str) -> redirect | render_template:
    """
    API ROUTE
    /user/<string:username>
    
    GET API
    Show a User their page

    :param username: The username to check
    :type username: str
    """
    # Get information about if the user is logged in and is querying the right user
    auth_status, proper_status, c_user = getUserAuthProperBothName(
        request, app_config, username
    )
    # If the user is logged in and is checking themselves
    if proper_status:
        return render_template("user.j2", logged_in=auth_status, user=username)
    # If they are a logged in and searching the wrong account reroute them to their account (Naughty! Naughty!)
    elif auth_status:
        return render_template("user.j2", logged_in=auth_status, user=c_user)
    # If neither reroute them to the login page
    else:
        # Remove any existing cookies
        user_redirect = redirect(url_for("auth.showLogin"))
        user_redirect.delete_cookie("user")
        user_redirect.delete_cookie("auth")
        return user_redirect

# Footer Comment
# History of Contributions:
# [2024-2025] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]