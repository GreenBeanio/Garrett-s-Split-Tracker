# Header Comment
# Project: [Garrett's Split Tracker] [https://github.com/GreenBeanio/Garrett-s-Split-Tracker]
# Copyright: Copyright (c) [2024]-[2025] [Garrett's Split Tracker] Contributors
# Version: [0.1]
# Status: [Development]
# License: [MIT]
# Author(s): [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Maintainer: [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Project Description: [This project is used to track "splits" in games or activities. With the ability to display them on a livestream.]
# File Description: [Sets up Celery periodic tasks]

# My Imports
from auth.functions.fn_removeExpiredSessions import removeExpiredSessions
from make_celery import celery_app

# Package Imports
from celery import Celery
import datetime

# Setting up the periodic functions after connecting
@celery_app.on_after_configure.connect
def setupPeriodic(sender: Celery, **kwargs) -> None:
    """
    Set Up Celery Periodic Tasks

    :param sender: A Celery worker to add tasks too
    :type sender: Celery
    :param kwargs: Additional Keyword Arguments for the task
    :type kwargs: Any

    :return: Nothing
    :rtype: None
    """
    # Create a task(s) to check for expired sessions
    # (timedelta or seconds [can also use a crontab like thing by importing crontab from celery],
    # the function with function.s(no parameters it seems), name for the task)

    # Check for expired sessions every minute
    sender.add_periodic_task(
        datetime.timedelta(minutes=1),
        removeExpiredSessions.s(),
        name="check-expired-sessions",
    )

# Footer Comment
# History of Contributions:
# [2024-2025] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]