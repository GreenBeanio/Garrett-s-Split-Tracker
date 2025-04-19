# Header Comment
# Project: [Garrett's Split Tracker] [https://github.com/GreenBeanio/Garrett-s-Split-Tracker]
# Copyright: Copyright (c) [2024]-[2025] [Garrett's Split Tracker] Contributors
# Version: [0.1]
# Status: [Development]
# License: [MIT]
# Author(s): [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Maintainer: [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Project Description: [This project is used to track "splits" in games or activities. With the ability to display them on a livestream.]
# File Description: [Creates a Redis Connection]

# Package Imports
import pathlib
import redis
from typing import Union

# Function to create Redis Connection
def connectRedis(
    connection_type: str,
    db: int,
    username: str,
    password: str,
    host: str,
    port: int,
    ssl_ca_certs: Union[pathlib.Path, None],
    ssl_certfile: Union[pathlib.Path, None],
    ssl_keyfile: Union[pathlib.Path, None],
) -> redis.Redis:  # Not sure on the type
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

    :return: Redis Connection
    :rtype: redis.Redis
    """
    # If there's no SSL
    if connection_type == "NO":
        redis_client = redis.Redis(
            db=db,
            username=username,
            password=password,
            host=host,
            port=port,
        )
    # If there's SSL
    elif connection_type == "PLAIN":
        redis_client = redis.Redis(
            db=db,
            username=username,
            password=password,
            host=host,
            port=port,
            ssl=True,
            # ssl_cert_reqs=???
        )
    # If there's SSL with Certificates
    elif connection_type == "CERTIFICATE":
        redis_client = redis.Redis(
            db=db,
            username=username,
            password=password,
            host=host,
            port=port,
            ssl=True,
            # ssl_cert_reqs=???
            ssl_ca_certs=ssl_ca_certs,
            ssl_certfile=ssl_certfile,
            ssl_keyfile=ssl_keyfile,
        )
    # Return the resulting connection
    return redis_client

# Footer Comment
# History of Contributions:
# [2024-2025] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]