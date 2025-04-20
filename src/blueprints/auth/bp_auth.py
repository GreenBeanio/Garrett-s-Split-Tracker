# Header Comment
# Project: [Garrett's Split Tracker] [https://github.com/GreenBeanio/Garrett-s-Split-Tracker]
# Copyright: Copyright (c) [2024]-[2024] [Garrett's Split Tracker] Contributors
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
from blueprints.auth.py.fn_checkUser import checkUser
from blueprints.auth.py.fn_createUser import createUser
from blueprints.auth.py.fn_createSalt import createSalt
from blueprints.auth.py.fn_generateAuth import generateAuth
from blueprints.auth.py.fn_getUserAuthStatus import getUserAuthStatus
from blueprints.auth.py.fn_checkLogin import checkLogin
from blueprints.auth.py.fn_getUserAuthProperBothName import getUserAuthProperBothName
from blueprints.auth.py.fn_removeSession import removeSession
from blueprints.auth.py.fn_removeAllUserSessions import removeAllUserSessions
from blueprints.auth.py.fn_getUserAuthCookiesStatusFull import getUserAuthCookiesStatusFull

# Package Imports
from flask import Blueprint, request, redirect, url_for, flash, make_response, render_template
from typing import Union

# Create the blueprint
auth_bp = Blueprint(
    "auth", # Set the name to call from Flask
    __name__, # Set the module name for local flask resources or something like that
    template_folder="templates", # This uses a templates folder in the same directory as the module
    static_folder="static", # Separate static folder for the blueprint
    static_url_path="/static/user", # Set the url path for the static files
    url_prefix="/user", # Set the URL prefix
    # subdomain="auth", # Don't believe I want a subdomain
)

# Tests the path
#print(auth_bp.root_path)

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
        return redirect(url_for("home.index"))
    
# Creating an interactive account creations page
@auth_bp.get("/new-user")
def newUser() -> Union[redirect, make_response]:
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
        return redirect(url_for("home.index"))
    
# Handling login attempts very crudely
@auth_bp.post("/login-attempt")
def loginAttempt() -> redirect: 
    """
    API ROUTE
    /login-attempt

    POST REQUEST
    Tests a login attempt.
    """
    n_user = request.form["user_box"]
    n_passw = request.form["pass_box"]
    ip_status = request.form.get("ip_check")
    print(ip_status)
    ip_addr = request.remote_addr
    if checkLogin(n_user, n_passw, app_config):
        # Generate auth
        age_s = 60 * 60  # 1 hour
        # Different auth depending on if we're using the IP or not
        if ip_status == "use_ip":
            auth = generateAuth(n_user, age_s, ip_addr, app_config)
        else:
            auth = generateAuth(n_user, age_s, "ignore", app_config)
        # Generate cookie
        user_redirect = redirect(url_for("auth.showUser", username=n_user))
        user_redirect.set_cookie("user", n_user, max_age=age_s)
        user_redirect.set_cookie("auth", auth, max_age=age_s)
        return user_redirect
    else:
        # I don't have these implemented yet, would probably actually want something in javascript so it doesn't delete their username every time
        flash("Unknown User or Incorrect Credentials")
        return redirect(url_for("auth.showLogin"))
    
# Creating the user page
@auth_bp.get("/user/<string:username>")
def showUser(username: str) -> Union[redirect, render_template]:
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
    
# Creating an interactive login page
@auth_bp.get("/login")
def showLogin() -> Union[redirect, make_response]:
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
        return redirect(url_for("home.index"))

# Footer Comment
# History of Contributions:
# [2024-2025] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]
