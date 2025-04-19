# Header Comment
# Project: [Garrett's Split Tracker] [https://github.com/GreenBeanio/Garrett-s-Split-Tracker]
# Copyright: Copyright (c) [2024]-[2025] [Garrett's Split Tracker] Contributors
# Version: [0.1]
# Status: [Development]
# License: [MIT]
# Author(s): [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Maintainer: [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Project Description: [This project is used to track "splits" in games or activities. With the ability to display them on a livestream.]
# File Description: [Creates a PostgreSQL Connection]

# Package Imports
import pathlib
import psycopg2
from typing import Union

# Function to create Postgre Connection
def connectPostgre(
    connection_type: str,
    database: str,
    user: str,
    password: str,
    host: str,
    port: int,
    sslrootcert: Union[pathlib.Path, None],
    sslcert: Union[pathlib.Path, None],
    sslkey: Union[pathlib.Path, None],
) -> psycopg2:  # Not sure on the type
    """
    Create a PostgreSQL Connection

    :param connection_type: The type of SSL connection. NO (None), PLAIN (username and password), 
    CA_CERTIFICATE (username, password, and SSL CA file), FULL_CERTIFICATE (username, password, and SSL files)
    :type connection_type: str
    :param database: The database name
    :type database: str
    :param user: The username
    :type user: str
    :param password: The password
    :type password: str
    :param host: The server host address
    :type host: str
    :param port: The server port
    :type port: int
    :param sslrootcert: The SSL ROOT FILE
    :type sslrootcert: Union[pathlib.Path, None]
    :param sslcert: The SSL CERT File
    :type sslcert: Union[pathlib.Path, None]
    :param sslkey: The SSL KEY File
    :type sslkey: Union[pathlib.Path, None]

    :return: PostgreSQL Connection
    :rtype: psycopg2
    """
    # If there's no SSL
    if connection_type == "NO":
        postgre_client = psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host=host,
            port=port,
        )
    # If there's SSL
    elif connection_type == "PLAIN":
        postgre_client = psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host=host,
            port=port,
            sslmode="require",
        )
    # If there's SSL verifying CA
    elif connection_type == "CA_CERTIFICATE":
        postgre_client = psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host=host,
            port=port,
            sslmode="verify-ca",
            sslrootcert=sslrootcert,
        )
    # If there's SSL verifying full
    elif connection_type == "FULL_CERTIFICATE":
        postgre_client = psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host=host,
            port=port,
            sslmode="verify-full",
            sslrootcert=sslrootcert,
            sslcert=sslcert,
            sslkey=sslkey,
        )
    # Return the resulting connection
    return postgre_client

# Footer Comment
# History of Contributions:
# [2024-2025] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]