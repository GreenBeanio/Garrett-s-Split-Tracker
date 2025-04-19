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
from auth.functions.fn_checkLogin import checkLogin
from auth.functions.fn_generateAuth import generateAuth 

# Package Imports
from flask import request, redirect, url_for, flash

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

# Footer Comment
# History of Contributions:
# [2024-2025] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]