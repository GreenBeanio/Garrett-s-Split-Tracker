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
import pymongo
import requests

# Test Users
users = [UserObj("GreenBeanio", "test1"), UserObj("GreenBeanio2", "test2")]
# Test sessions
sessions = {"false": "rhjaudfbasudfb"}

# Creating the flask app
app = Flask(__name__)
app.testing = True
app.secret_key = "ILoveFrogs"  # Obviously for testing don't hardcode this


# Creating the main page
@app.route("/")
def index():
    # Checking if you're already logged in
    u_user = request.cookies.get("user")
    u_auth = request.cookies.get("auth")
    status = checkAuth(u_user, u_auth, sessions)
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


# Creating the user page
@app.get("/user/<string:username>")
def showUser(username):
    # Checking the users authentication
    u_user = request.cookies.get("user")
    u_auth = request.cookies.get("auth")
    status = checkAuth(u_user, u_auth, sessions)
    if status:
        return render_template("user.j2", t_user=username)
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
    # Checking if you're already logged in
    u_user = request.cookies.get("user")
    u_auth = request.cookies.get("auth")
    status = checkAuth(u_user, u_auth, sessions)
    if not status:
        # Remove any existing cookies
        user_render = make_response(render_template("login.j2"))
        user_render.delete_cookie("user")
        user_render.delete_cookie("auth")
        return user_render
    else:
        flash("You're already logged in")
        return redirect(url_for("index"))


# Handling login attempts very crudely
@app.post("/login_attempt")
def login_attempt():
    test_u = request.form["user_box"]
    test_p = request.form["pass_box"]
    user = checkUser(test_u, test_p, users)
    if user is not None:
        # Generate auth
        age_s = 60 * 60  # 1 hour
        auth = generateAuth(test_u, test_p, age_s, sessions)
        # Generate cookie
        user_redirect = redirect(url_for("showUser", username=test_u))
        user_redirect.set_cookie("user", test_u, max_age=age_s)
        user_redirect.set_cookie("auth", auth, max_age=age_s)
        return user_redirect
    else:
        # I don't have these implemented yet, would probably actually want something in javascript so it doesn't delete their username every time
        flash("Unknown User or Incorrect Credentials")
        return redirect(url_for("show_login"))


# Creating an interactive log out page
@app.route("/logout", methods=["GET", "POST"])
def show_logout():
    if request.method == "GET":
        # Checking if you're already logged in
        u_user = request.cookies.get("user")
        u_auth = request.cookies.get("auth")
        status = checkAuth(u_user, u_auth, sessions)
        if status:
            return render_template("logout.j2", user_t=u_user, session_t=u_auth)
        else:
            flash("You aren't logged in")
            return redirect(url_for("show_login"))
    elif request.method == "POST":
        # Get the items we basically just sent. This is stupid, but it's the best I can think of with my JavaScript inexperience and tiredness.
        test_u = request.form["user_box"]
        test_a = request.form["session_box"]
        # Delete the session
        del sessions[test_u]
        # I think I'd want this to actually log out of the current session so not like this. I'd also probably need to pass the session in.
        # Go to the log in
        flash("You've been logged out")
        return redirect(url_for("show_login"))


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
