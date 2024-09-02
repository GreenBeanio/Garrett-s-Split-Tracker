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
from auth.functions.auth_functions import getUserAuthProperBothName

# New Imports
from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import make_response
from flask import url_for
from flask import flash
from markupsafe import escape

# # Package Imports
# from flask import Flask
# from markupsafe import escape
# from flask import url_for
# from flask import request
# from flask import render_template
# from markupsafe import Markup
# from flask import make_response
# from flask import session
# from flask import redirect
# from flask import jsonify
# from flask import flash
# from celery import Celery
# from celery import Task
# from celery import shared_task
# from celery.result import AsyncResult

# # Future imports
# import pandas
# import matplotlib
# from pydantic import BaseModel
# import typing
# import dataclasses
# from pymongo import MongoClient
# import requests

# Create the blueprint
auth_bp = Blueprint(
    "auth",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static/auth",
    url_prefix="/user",
    # subdomain="auth",
)

###
# Note: huge problem is that right now seemingly if you authenticate a session for any user it'll let you go to any users page!
# Just have it check you're going to your page or not. Something like that
###


# Creating the user page
@auth_bp.get("/user/<string:username>")
def showUser(username):
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


# Creating an interactive login page
@auth_bp.get("/login")
def showLogin():
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


# Handling login attempts very crudely
@auth_bp.post("/login-attempt")
def loginAttempt():
    n_user = request.form["user_box"]
    n_passw = request.form["pass_box"]
    c_passw = request.form["confirm_pass_box"]
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


# Creating an interactive log out page
@auth_bp.route("/logout", methods=["GET", "POST"])
def showLogout():
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


# Creating an interactive account creations page
@auth_bp.get("/new-user")
def newUser():
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


# Handling attempts to create users very crudely
@auth_bp.post("/create-attempt")
def createAttempt():
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
# [2024-2024] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]
