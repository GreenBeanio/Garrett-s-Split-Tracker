# Header Comment
# Project: [Garrett's Split Tracker] [https://github.com/GreenBeanio/Garrett-s-Split-Tracker]
# Copyright: Copyright (c) [2024]-[2025] [Garrett's Split Tracker] Contributors
# Version: [0.1]
# Status: [Development]
# License: [MIT]
# Author(s): [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Maintainer: [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Project Description: [This project is used to track "splits" in games or activities. With the ability to display them on a livestream.]
# File Description: [Creates a MongoDB Connection]

# Package Imports
import pathlib
from pymongo import MongoClient
from typing import Union

# Function to create Mongo Connection
def connectMongo(
    connection_type: str,
    authSource: str,
    username: str,
    password: str,
    host: str,
    port: int,
    tlsCAFile: Union[pathlib.Path, None],
    tlsCertificateKeyFile: Union[pathlib.Path, None],
) -> MongoClient:
    """
    Create a MongoDB Connection

    :param connection_type: The type of SSL connection. NO (None), PLAIN (username and password), 
    CERTIFICATE(username, password, and SSL files)
    :type connection_type: str
    :param authSource: The database name
    :type authSource: str
    :param username: The username
    :type username: str
    :param password: The password
    :type password: str
    :param host: The server host address
    :type host: str
    :param port: The server port
    :type port: int
    :param tlsCAFile: The SSL CA file
    :type tlsCAFile: Union[pathlib.Path, None]
    :param tlsCertificateKeyFile: The SSL KEY file
    :type tlsCertificateKeyFile: Union[pathlib.Path, None]

    :return: The MongoDB Connection
    :rtype: MongoClient
    """ 
    # If there's no SSL
    if connection_type == "NO":
        mongo_client = MongoClient(
            authSource=authSource,
            username=username,
            password=password,
            host=host,
            port=port,
        )
    # If there's SSL
    elif connection_type == "PLAIN":
        mongo_client = MongoClient(
            authSource=authSource,
            username=username,
            password=password,
            host=host,
            port=port,
            tls=True,
        )
    # If there's SSL with Certificates
    elif connection_type == "CERTIFICATE":
        mongo_client = MongoClient(
            authSource=authSource,
            username=username,
            password=password,
            host=host,
            port=port,
            tls=True,
            tlsCAFile=tlsCAFile,
            tlsCertificateKeyFile=tlsCertificateKeyFile,
        )
    # print(f'mongodb://{json_obj["MONGO_USER"]}:{json_obj["MONGO_PASS"]}@{json_obj["MONGO_ADDRESS"]}:{json_obj["MONGO_PORT"]}/?authSource={json_obj["MONGO_DATABASE"]}&tls=true&tlsCAFILE={json_obj["MONGO_SSL_FILE"]}')
    # print(f'mongodb://{json_obj["MONGO_USER"]}:{json_obj["MONGO_PASS"]}@{json_obj["MONGO_ADDRESS"]}:{json_obj["MONGO_PORT"]}/?authSource={json_obj["MONGO_DATABASE"]}')
    # print(mongo_client)
    # print(mongo_client.server_info())
    # Return the resulting connection
    return mongo_client

# Footer Comment
# History of Contributions:
# [2024-2025] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]