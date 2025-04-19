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
from auth.functions.fn_getUserAuthCookiesStatusFull import getUserAuthCookiesStatusFull
from auth.functions.fn_removeAllUserSessions import removeAllUserSessions
from auth.functions.fn_removeSession import removeSession

# Package Imports
from flask import render_template, request, redirect, url_for, flash

# Creating an interactive log out page
@auth_bp.route("/logout", methods=["GET", "POST"])
def showLogout() -> redirect:
    """
    API ROUTE
    /logout
    
    GET REQUEST
    Show the logout page in logged in.
    Show the login page if not logged in.
    
    POST REQUEST
    Logout the User and remove the Session.
    """
    # Get cookie information
    c_user, c_auth, auth_status = getUserAuthCookiesStatusFull(request, app_config)
    if request.method == "GET":
        # Checking if you're already logged in
        if auth_status:
            return render_template(
                "logout.j2", logged_in=auth_status, user=c_user, session=c_auth
            )
        else:
            flash("You aren't logged in")
            return redirect(url_for("auth.showLogin"))
    elif request.method == "POST":
        # I wasn't checking for auth before on this because this shouldn't get called without auth, but just in case someone
        # does some shenanigans and tries to call it directly. Even so if they were able to do it somehow it still wouldn't do anything
        # besides try and remove a session.
        if auth_status:
            # Check if the user wants to log out of all sessions (Getting the checkbox result) [Doing it with the get method instead of the index-like method
            # because if it's not checked it will be None. If you have multiple items with the same name use getlist]
            user = request.form.get("log_all_check")
            if user == "log_out_all":
                # Delete all the user sessions
                removeAllUserSessions(c_user, app_config)
            else:
                # Delete only the current session
                removeSession(c_user, c_auth, app_config)
        # I think I'd want this to actually log out of the current session so not like this. I'd also probably need to pass the session in.
        # Go to the log in
        flash("You've been logged out")
        return redirect(url_for("auth.showLogin"))

# Footer Comment
# History of Contributions:
# [2024-2025] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]