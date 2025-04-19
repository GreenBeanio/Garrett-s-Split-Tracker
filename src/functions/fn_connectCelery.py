# Header Comment
# Project: [Garrett's Split Tracker] [https://github.com/GreenBeanio/Garrett-s-Split-Tracker]
# Copyright: Copyright (c) [2024]-[2025] [Garrett's Split Tracker] Contributors
# Version: [0.1]
# Status: [Development]
# License: [MIT]
# Author(s): [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Maintainer: [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Project Description: [This project is used to track "splits" in games or activities. With the ability to display them on a livestream.]
# File Description: [Creates a Celery Connection]

# Package Imports
import pathlib
from typing import Union
import ssl

# Function to create Celery Connection
def connectCelery(
    connection_type: str,
    db: int,
    username: str,
    password: str,
    host: str,
    port: int,
    ssl_ca_certs: Union[pathlib.Path, None],
    ssl_certfile: Union[pathlib.Path, None],
    ssl_keyfile: Union[pathlib.Path, None],
) -> dict:
    """
    Create a Redis Connection

    :param connection_type: The type of SSL connection. NO (None), PLAIN (username and password), 
    CERTIFICATE (username, password, and SSL files)
    :type connection_type: str
    :param db: The database name
    :type db: str
    :param username: The username
    :type username: str
    :param password: The password
    :type password: str
    :param host: The server host address
    :type host: str
    :param port: The server port
    :type port: int
    :param ssl_ca_certs: The SSL CA FILE
    :type ssl_ca_certs: Union[pathlib.Path, None]
    :param ssl_certfile: The SSL CERT File
    :type ssl_certfile: Union[pathlib.Path, None]
    :param ssl_keyfile: The SSL KEY File
    :type ssl_keyfile: Union[pathlib.Path, None]

    :return: Celery dictionary
    :rtype: dict
    """
    # If there's no SSL
    if connection_type == "NO":
        # Create the celery dict
        redis_uri = f"redis://{username}:{password}@{host}:{port}/{db}"
        celery_dict = dict(
            broker_url=redis_uri,
            result_backend=redis_uri,
            task_ignore_result=True,
            task_default_queue="split_tracker",  # Not sure if this is right, but I'm testing it
            # Beat schedule for timing repetitive events (You can set up the schedules in here like this too instead of with the functions)
            # "task-name" : {"task": "function", "schedule": time_in_seconds}
            # beat_schedule={
            #     "task-every-minute": {
            #         "task": "auth.functions.auth_functions.removeExpiredSessions",
            #         "schedule": datetime.timedelta(seconds=1),
            #     }
            # },
        )
    # If there's SSL
    elif connection_type == "PLAIN":
        # Create the celery dict
        redis_uri = f"redis://{username}:{password}@{host}:{port}/{db}"
        celery_dict = dict(
            broker_url=redis_uri,
            result_backend=redis_uri,
            task_ignore_result=True,
            task_default_queue="split_tracker",  # Not sure if this is right, but I'm testing it
            # Beat schedule for timing repetitive events (You can set up the schedules in here like this too instead of with the functions)
            # "task-name" : {"task": "function", "schedule": time_in_seconds}
            # beat_schedule={
            #     "task-every-minute": {
            #         "task": "auth.functions.auth_functions.removeExpiredSessions",
            #         "schedule": datetime.timedelta(seconds=1),
            #     }
            # },
            broker_use_ssl={
                "keyfile": ssl_keyfile,
                "certfile": ssl_certfile,
                "ca_certs": ssl_ca_certs,
                "cert_reqs": ssl.CERT_NONE,  # Maybe set this to "ssl.CERT_OPTIONAL" instead
            },
        )
    # If there's SSL with Certificates
    elif connection_type == "CERTIFICATE":
        # Create the celery dict
        redis_uri = f"redis://{username}:{password}@{host}:{port}/{db}"
        celery_dict = dict(
            broker_url=redis_uri,
            result_backend=redis_uri,
            task_ignore_result=True,
            task_default_queue="split_tracker",  # Not sure if this is right, but I'm testing it
            # Beat schedule for timing repetitive events (You can set up the schedules in here like this too instead of with the functions)
            # "task-name" : {"task": "function", "schedule": time_in_seconds}
            # beat_schedule={
            #     "task-every-minute": {
            #         "task": "auth.functions.auth_functions.removeExpiredSessions",
            #         "schedule": datetime.timedelta(seconds=1),
            #     }
            # },
            broker_use_ssl={
                "keyfile": ssl_keyfile,
                "certfile": ssl_certfile,
                "ca_certs": ssl_ca_certs,
                "cert_reqs": ssl.CERT_REQUIRED,
            },
        )
    # Return the resulting dictionary
    return celery_dict

# Footer Comment
# History of Contributions:
# [2024-2025] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]