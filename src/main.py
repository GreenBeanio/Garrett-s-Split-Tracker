# Imports

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
import datetime
import zoneinfo
import hashlib

# Future imports

import pandas
import matplotlib
from pydantic import BaseModel
import typing
import dataclasses
import pymongo
import requests

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
    status = Check_Auth(u_user, u_auth)
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
def show_user(username):
    # Checking the users authentication
    u_user = request.cookies.get("user")
    u_auth = request.cookies.get("auth")
    status = Check_Auth(u_user, u_auth)
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
    status = Check_Auth(u_user, u_auth)
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
    user = Check_User(test_u, test_p)
    if user is not None:
        # Generate auth
        age_s = 60 * 60  # 1 hour
        auth = Generate_Auth(test_u, test_p, age_s)
        # Generate cookie
        user_redirect = redirect(url_for("show_user", username=test_u))
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
        status = Check_Auth(u_user, u_auth)
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


# test class just to store users
class user_obj:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password


# Test class to store sessions for authentication
class user_auth:
    def __init__(self, user: str, auth: str, exp: datetime):
        self.user = user
        self.auth = auth
        self.exp = exp


# Test Users
users = [user_obj("GreenBeanio", "test1"), user_obj("GreenBeanio2", "test2")]
# Test sessions
sessions = {"false": "rhjaudfbasudfb"}


# Test to check users
def Check_User(username: str, password: str):
    for user in users:
        if user.username == username and user.password == password:
            return user
    return None


# Test to check authentication
def Check_Auth(user: str, auth: str) -> bool:
    # Check all sessions to see if a user has a session
    for s_user, s_auth in sessions.items():
        # Checking this because I'd like to have multiple sessions per user in the future ... maybe
        if s_user == user:
            # From the session object check the auth cookie
            if s_auth.auth == auth:
                # Check if the session has expired or not
                ct = datetime.datetime.now(datetime.timezone.utc)
                if s_auth.exp >= ct:
                    return True
                # If it isn't then delete the session
                else:
                    del sessions[s_user]
    return False


# Test to generate auth
def Generate_Auth(user: str, passw: str, age_s: int) -> str:
    # Creating the expiration date
    exp = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        seconds=age_s
    )
    # Get a string of the current date time
    auth_s = str(exp) + user + passw
    auth_h = hashlib.sha256(auth_s.encode("utf-8")).hexdigest()
    # Saving the auth
    auth = user_auth(user, auth_h, exp)
    # In production I would add this to a database, technically I don't even need to add the user in the class because it's stored as the key
    # Although it'd like to actually be able to have multiple sessions possibly. For if using on two devices. I suppose I could
    # grab the session id from the database instead too.
    sessions.update({user: auth})
    # Returning the auth for a cookie
    return auth_h


# Testing the urls
with app.test_request_context():
    print(url_for("index"))
    print(url_for("show_user", username="GreenBeanio"))
    print(url_for("show_tracker", username="GreenBeanio"))
    print(
        url_for("show_tracked_activity", username="GreenBeanio", activity="Programming")
    )
    print(url_for("login_attempt"))

# Creating a test static file for css
# url_for("static", filename="style.css")
