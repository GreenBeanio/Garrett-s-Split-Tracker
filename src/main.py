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

# Future imports

import pandas
import matplotlib
from pydantic import BaseModel
import typing
import dataclasses
import pymongo

# Creating the flask app
app = Flask(__name__)


# Creating the main page
@app.route("/")
def index():
    return "<p>Hello!</p>"


# Creating the user page
@app.route("/user")
@app.route("/user/<string:username>", methods=["GET", "POST"])
def show_user(username=None):
    if request.method == "GET":
        print(f"User is getting {escape(username)}")
        return render_template("user.j2", t_user=username)
    elif request.method == "POST":
        print(f"User is posting {escape(username)}")
        return render_template("user.j2", t_user=username)


# Creating the tracker page
@app.route("/tracker/<string:username>")
def show_tracker(username):
    return f"User is {escape(username)}"


# Creating the specific tracked activity page
@app.route("/tracker/<string:username>/<string:activity>")
def show_tracked_activity(username, activity):
    return f"User is {escape(username)} for the activity {escape(activity)}"


# Creating a test get http method
@app.get("/user/<string:username>")
def get_user():
    return "Getting user"


# Creating a test post http method
@app.post("/user/<string:username>")
def post_user():
    return "Posting user"


# Creating a test static file for css
# url_for("static", filename="style.css")

### Trying to actually experiment more now ###


# Creating an interactive login page
@app.route(
    "/login",
)
def show_login():
    return render_template("login.j2")


# Handling login attempts very crudely
@app.route("/login_attempt", methods=["GET", "POST"])
def login_attempt():
    if request.method == "GET":
        test_u = request.args["user_box"]
        test_p = request.args["pass_box"]
        print(f"GET: {test_u} {test_p}")
        return redirect("login")

    if request.method == "POST":
        test_u = request.form["user_box"]
        test_p = request.form["pass_box"]
        print(f"POST: {test_u} {test_p}")
        user = Check_User(test_u, test_p)
        if user is not None:
            return redirect(url_for("show_user", username=test_u))
        else:
            return "Not a known user"

    return "I've made a grave mistake"


# test class just to store users
class user_obj:
    def __init__(self, username, password):
        self.username = username
        self.password = password


# Test Users
users = [user_obj("GreenBeanio", "test1"), user_obj("GreenBeanio2", "test2")]


# Test to check users
def Check_User(username: str, password: str):
    for user in users:
        if user.username == username and user.password == password:
            print("matched")
            return user
    return None


# # Creating a test get http method
# @app.get("/login")
# def get_login():
#     print("hi")
#     return "Getting user"


# # Creating a test post http method
# @app.post("/login")
# def post_login():
#     return "Posting user"

# Testing the urls
with app.test_request_context():
    print(url_for("index"))
    print(url_for("show_user", username="GreenBeanio"))
    print(url_for("show_tracker", username="GreenBeanio"))
    print(
        url_for("show_tracked_activity", username="GreenBeanio", activity="Programming")
    )
    print(url_for("login_attempt"))
