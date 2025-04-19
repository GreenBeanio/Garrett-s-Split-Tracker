# Header Comment
# Project: [Garrett's Split Tracker] [https://github.com/GreenBeanio/Garrett-s-Split-Tracker]
# Copyright: Copyright (c) [2024]-[2025] [Garrett's Split Tracker] Contributors
# Version: [0.1]
# Status: [Development]
# License: [MIT]
# Author(s): [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Maintainer: [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Project Description: [This project is used to track "splits" in games or activities. With the ability to display them on a livestream.]
# File Description: [A file holding many functions used in the auth module.]

# Import Credentials
from stored_credentials import app_config

# Package Imports
import datetime
from celery import shared_task

# Repeated task to remove expired sessions (currently running once an hour, if they try to connect with an expired session before that it'll be removed anyway)
# (This function is comment hell as a warning)
@shared_task()  # (ignore_result=False)
def removeExpiredSessions() -> None:
    """
    Removes all expired sessions from the MongoDB database
    """
    # Get the mongodb session
    mongo_db = app_config.mongo_con.get_database("split_tracker").get_collection(
        "sessions"
    )
    # Check that there are sessions before committing
    # (I could also do "len(list(sessions)) > 0", but I think the mongo query is probably faster than the conversion)
    # (I could also query time in mongodb, but I'm doing it in python in case there's time wumbo jumbo differences between the two)
    session_count = mongo_db.count_documents({})
    if session_count > 0:
        # Get all the sessions
        sessions = mongo_db.find({})
        # Iterate over the sessions
        for session in sessions:
            # # Testing time zones
            # local_tz = (
            #     datetime.datetime.now().astimezone().tzinfo
            # )  # Gets the local time zone
            # now = datetime.datetime.now(
            #     local_tz
            # )  # Get the local time that's time zone aware
            # print(datetime.datetime.tzname(now))  # Gets the timezone from a datetime
            # print(
            #     now.astimezone(tz=datetime.timezone.utc)
            # )  # Converts the time zone (gives the correct adjusted datetime)
            # print(
            #     now.replace(tzinfo=datetime.timezone.utc)
            # )  # Replaces the time zone (doesn't adjust the datetime just replaces the offset from the time zone! Probably not what you want!)
            # Extract the time and change the timezone (using replace because they should've been saved in UTC)
            exp = session["exp"].replace(tzinfo=datetime.timezone.utc)
            # Get the current time
            now = datetime.datetime.now(datetime.datetime.now().astimezone().tzinfo)
            # # Testing the different time zones methods again
            # dif = now - exp  # Gives the time you'd expect between the two time zones
            # dif2 = (
            #     now.astimezone(tz=datetime.timezone.utc) - exp
            # )  # Gives the same time because the datetimes have been adjusted
            # dif3 = (
            #     now.replace(tzinfo=datetime.timezone.utc) - exp
            # )  # Gives the wrong timedelta because the timezone was replaced not adjusted
            # print(dif)
            # print(dif2)
            # print(dif3)
            # dt_plain = datetime.datetime.now() # date time that is naive and has no time zone
            # dt_utc = datetime.datetime.now(datetime.timezone.utc) # Time zone that has the time adjusted for the given timezone (it works!)
            # dt_local = datetime.datetime.now(
            #     datetime.datetime.now().astimezone().tzinfo
            # ) # Time zone with your local time and time zone
            # If the expiration time is smaller than the current time delete it
            if exp <= now:
                # Delete based on the session id because it's guaranteed to be the most unique (even though auth should be as well)
                mongo_db.delete_one({"_id": session["_id"]})
    # # Testing debug methods since print doesn't work with the beat task
    # # Testing method 1
    # from celery.utils.log import get_task_logger
    # logger = get_task_logger(__name__)
    # logger.info("Method 1")
    # logger.info(sessions)
    # import logging
    # # Testing method 2
    # logger2 = logging.getLogger()
    # logger2.info("Method 2")
    # logger2.info(sessions)
    # # Testing method 3
    # print("Method 3")
    # print(sessions)
    # # They all worked actually I was tripping. They just show up in the celery worker console and not through flask.
    # # Kind of annoying, but it is what it is


# # Check the celery task name
# print(removeExpiredSessions.name)

# Footer Comment
# History of Contributions:
# [2024-2025] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]