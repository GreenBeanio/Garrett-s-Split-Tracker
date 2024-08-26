# Header Comment
# Project: [Garrett's Split Tracker] [https://github.com/GreenBeanio/Garrett-s-Split-Tracker]
# Copyright: Copyright (c) [2024]-[2024] [Garrett's Split Tracker] Contributors
# Version: [0.1]
# Status: [Development]
# License: [MIT]
# Author(s): [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Maintainer: [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Project Description: [This project is used to track "splits" in games or activities. With the ability to display them on a livestream.]
# File Description: [The main file to run flask and other core components.]


# My imports
from py.classes import *
from py.functions import *
from py.create_apps import createFlaskApp

# Package Imports
from flask import Flask
from markupsafe import escape
from flask import url_for
from flask import request
from flask import render_template
from markupsafe import Markup
from flask import make_response
from flask import session
from flask import redirect
from flask import jsonify
from flask import flash
from celery import Celery
from celery import Task

# Future imports
import pandas
import matplotlib
from pydantic import BaseModel
import typing
import dataclasses
from pymongo import MongoClient
import requests

# Get the config
app_config = loadCredentials(__file__)  # Using the location of this main file

# Create the apps
flask_app = createFlaskApp(__name__, app_config)
celery_app = flask_app.extensions["celery"]


# Creating the main page
@flask_app.route("/")
def index():
    # Checking if you're already logged in
    u_user = request.cookies.get("user")
    u_auth = request.cookies.get("auth")
    status = checkAuth(u_user, u_auth, app_config)
    if status:
        return render_template("home.j2", t_user=u_user)
    # If you're not logged in go to the log in menu
    else:
        flash("Please log in")
        # Remove any existing cookies
        user_redirect = redirect(url_for("showLogin"))
        user_redirect.delete_cookie("user")
        user_redirect.delete_cookie("auth")
        return user_redirect


###
# Note: huge problem is that right now seemingly if you authenticate a session for any user it'll let you go to any users page!
# Just have it check you're going to your page or not. Something like that
###


# Creating the user page
@flask_app.get("/user/<string:username>")
def showUser(username):
    # Checking the users authentication
    u_user = request.cookies.get("user")
    u_auth = request.cookies.get("auth")
    if checkAuth(u_user, u_auth, app_config):
        # Check to make sure you're going to your own account and not someone else's like a bad boy.
        if username == u_user:
            return render_template("user.j2", t_user=username)
        else:
            # Temporary solution... this won't work because they could just edit the username in their cookies... I need to
            # have it check the session auth for the username in question. I'm tired now though and it's time for bed. That's
            # a problem for me to fix tomorrow.
            # You know storing this as a cookie is probably a bad security idea, but I'm just trying to learn flask right now.
            # Security for my personal project can come after I figure it out. I suppose I could store this data in the session
            # object from flask, but I want it to be saved so they don't have to login again. You can set the session to not
            # disappear though. Cookies may be foolish, but oh well. Pretty sure roblox uses one for session security and
            # they surely know more than me.
            return "Naughty Boy"
    else:
        flash("Unknown User or Incorrect Credentials")
        # Remove any existing cookies
        user_redirect = redirect(url_for("showLogin"))
        user_redirect.delete_cookie("user")
        user_redirect.delete_cookie("auth")
        return user_redirect


# Creating the tracker page
@flask_app.route("/tracker/<string:username>")
def showTracker(username):
    return f"User is {escape(username)}"


# Creating the specific tracked activity page
@flask_app.route("/tracker/<string:username>/<string:activity>")
def showTrackedActivity(username, activity):
    return f"User is {escape(username)} for the activity {escape(activity)}"


# Creating an interactive login page
@flask_app.route("/login")
def showLogin():
    # Checking if you're already logged in (on their browser)
    u_user = request.cookies.get("user")
    u_auth = request.cookies.get("auth")
    # If the user isn't already logged in
    if not checkAuth(u_user, u_auth, app_config):
        # Remove any existing cookies
        user_render = make_response(render_template("login.j2"))
        user_render.delete_cookie("user")
        user_render.delete_cookie("auth")
        return user_render
    # If they are already logged in
    else:
        flash("You're already logged in")
        return redirect(url_for("index"))


# Handling login attempts very crudely
@flask_app.post("/loginAttempt")
def loginAttempt():
    user = request.form["user_box"]
    passw = request.form["pass_box"]
    if checkLogin(user, passw, app_config):
        # Generate auth
        age_s = 60 * 60  # 1 hour
        auth = generateAuth(user, age_s, app_config)
        # Generate cookie
        user_redirect = redirect(url_for("showUser", username=user))
        user_redirect.set_cookie("user", user, max_age=age_s)
        user_redirect.set_cookie("auth", auth, max_age=age_s)
        return user_redirect
    else:
        # I don't have these implemented yet, would probably actually want something in javascript so it doesn't delete their username every time
        flash("Unknown User or Incorrect Credentials")
        return redirect(url_for("showLogin"))


# Creating an interactive log out page
@flask_app.route("/logout", methods=["GET", "POST"])
def showLogout():
    # Checking if you're already logged in
    u_user = request.cookies.get("user")
    u_auth = request.cookies.get("auth")
    if request.method == "GET":
        status = checkAuth(u_user, u_auth, app_config)
        if status:
            return render_template("logout.j2", user_t=u_user, session_t=u_auth)
        else:
            flash("You aren't logged in")
            return redirect(url_for("showLogin"))
    elif request.method == "POST":
        # Get the items we basically just sent. This is stupid, but it's the best I can think of with my JavaScript inexperience and tiredness.
        user = request.form["user_box"]
        # Delete the session
        removeSession(user, u_auth, app_config)
        # I think I'd want this to actually log out of the current session so not like this. I'd also probably need to pass the session in.
        # Go to the log in
        flash("You've been logged out")
        return redirect(url_for("showLogin"))


# Creating an interactive account creations page
@flask_app.route("/new_user")
def newUser():
    # Checking if you're already logged in
    u_user = request.cookies.get("user")
    u_auth = request.cookies.get("auth")
    status = checkAuth(u_user, u_auth, app_config)
    if not status:
        # Remove any existing cookies
        user_render = make_response(render_template("new_user.j2"))
        user_render.delete_cookie("user")
        user_render.delete_cookie("auth")
        return user_render
    else:
        flash("You're already logged in")
        return redirect(url_for("index"))


# Handling attempts to create users very crudely
@flask_app.post("/createAttempt")
def createAttempt():
    user = request.form["user_box"]
    passw = request.form["pass_box"]
    # Check if the user doesn't already exist
    if not checkUser(user, app_config):
        # Generate a new user and their salt
        createUser(user, passw, createSalt(), app_config)
        # Generate auth for the new user
        age_s = 60 * 60  # 1 hour
        auth = generateAuth(user, age_s, app_config)
        # Generate cookie
        user_redirect = redirect(url_for("showUser", username=user))
        user_redirect.set_cookie("user", user, max_age=age_s)
        user_redirect.set_cookie("auth", auth, max_age=age_s)
        return user_redirect
    else:
        flash("User already exists")
        return redirect(url_for("index"))


# Test out a celery task
@celery_app.task
def checkSessions():
    print("hi")


task = checkSessions.delay()

# Start the app
if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=5000, debug=True)

# Footer Comment
# History of Contributions:
# [2024-2024] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]
