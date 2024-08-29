# Header Comment
# Project: [Garrett's Split Tracker] [https://github.com/GreenBeanio/Garrett-s-Split-Tracker]
# Copyright: Copyright (c) [2024]-[2024] [Garrett's Split Tracker] Contributors
# Version: [0.1]
# Status: [Development]
# License: [MIT]
# Author(s): [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Maintainer: [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Project Description: [This project is used to track "splits" in games or activities. With the ability to display them on a livestream.]
# File Description: [Used to create celery workers]

# My imports
from main import createFlaskApp
from stored_credentials import app_config

# Imports for celery beats
from auth.functions.auth_functions import removeExpiredSessions

# Imports
from celery import Celery
import datetime

# Make a celery worker
# app_config = loadCredentials(__file__)  # Using the location of this main file
flask_app = createFlaskApp(app_config)
celery_app: Celery = flask_app.extensions["celery"]


# Setting up the periodic functions after connecting
@celery_app.on_after_configure.connect
def setup_periodic(sender, **kwargs):
    # Create a task(s) to check for expired sessions
    # (timedelta or seconds [can also use a crontab like thing by importing crontab from celery],
    # the function with function.s(no parameters it seems), name for the task)

    # Check for expired sessions every minute
    sender.add_periodic_task(
        datetime.timedelta(minutes=1),
        removeExpiredSessions.s(),
        name="check-expired-sessions",
    )


# Run the function to set it up (You can also set these up in the configuration, but I prefer this way for now)
setup_periodic(celery_app)

##### Test Shit ####

# # Test out a celery task (Shit still doesn't work!)
# @shared_task(
#     ignore_result=False
# )  # , name="auth.functions.auth_functions.removeExpiredSessions"
# def checkSessions(x) -> str:
#     return x


# result = checkSessions.delay("hi")
# result_result = AsyncResult(result.id)
# print(result_result.ready())
# print(result_result.successful())
# print(result_result.result)
# print(result_result.get())

##### End Test Shit ####

# Footer Comment
# History of Contributions:
# [2024-2024] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]
