# My imports
from py.classes import *
from py.functions import *

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


# Future imports
import pandas
import matplotlib
from pydantic import BaseModel
import typing
import dataclasses
from pymongo import MongoClient
import requests

# Load the config
app_config = loadCredentials(__file__)  # Using the location of this main file

# Creating the flask app
app = Flask(__name__)
app.testing = True
app.secret_key = app_config.secret_key


# Creating the main page
@app.route("/")
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
        user_redirect = redirect(url_for("show_login"))
        user_redirect.delete_cookie("user")
        user_redirect.delete_cookie("auth")
        return user_redirect


###
# Note: huge problem is that right now seemingly if you authenticate a session for any user it'll let you go to any users page!
# Just have it check you're going to your page or not. Something like that
###


# Creating the user page
@app.get("/user/<string:username>")
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
        user_redirect = redirect(url_for("show_login"))
        user_redirect.delete_cookie("user")
        user_redirect.delete_cookie("auth")
        return user_redirect


# Creating the tracker page
@app.route("/tracker/<string:username>")
def show_tracker(username):
    return f"User is {escape(username)}"


# Creating the specific tracked activity page
@app.route("/tracker/<string:username>/<string:activity>")
def show_tracked_activity(username, activity):
    return f"User is {escape(username)} for the activity {escape(activity)}"


# Creating an interactive login page
@app.route("/login")
def show_login():
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
@app.post("/login_attempt")
def login_attempt():
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
        return redirect(url_for("show_login"))


# Creating an interactive log out page
@app.route("/logout", methods=["GET", "POST"])
def show_logout():
    # Checking if you're already logged in
    u_user = request.cookies.get("user")
    u_auth = request.cookies.get("auth")
    if request.method == "GET":
        status = checkAuth(u_user, u_auth, app_config)
        if status:
            return render_template("logout.j2", user_t=u_user, session_t=u_auth)
        else:
            flash("You aren't logged in")
            return redirect(url_for("show_login"))
    elif request.method == "POST":
        # Get the items we basically just sent. This is stupid, but it's the best I can think of with my JavaScript inexperience and tiredness.
        user = request.form["user_box"]
        # Delete the session
        removeSession(user, u_auth, app_config)
        # I think I'd want this to actually log out of the current session so not like this. I'd also probably need to pass the session in.
        # Go to the log in
        flash("You've been logged out")
        return redirect(url_for("show_login"))


# Creating an interactive account creations page
@app.route("/new_user")
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
@app.post("/create_attempt")
def create_attempt():
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


# Testing the urls
with app.test_request_context():
    print(url_for("index"))
    print(url_for("showUser", username="GreenBeanio"))
    print(url_for("show_tracker", username="GreenBeanio"))
    print(
        url_for("show_tracked_activity", username="GreenBeanio", activity="Programming")
    )
    print(url_for("login_attempt"))

# Creating a test static file for css
# url_for("static", filename="style.css")

# Start the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
