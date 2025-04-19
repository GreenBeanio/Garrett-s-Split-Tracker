# Header Comment
# Project: [Garrett's Split Tracker] [https://github.com/GreenBeanio/Garrett-s-Split-Tracker]
# Copyright: Copyright (c) [2024]-[2024] [Garrett's Split Tracker] Contributors
# Version: [0.1]
# Status: [Development]
# License: [MIT]
# Author(s): [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Maintainer: [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Project Description: [This project is used to track "splits" in games or activities. With the ability to display them on a livestream.]
# File Description: [Class for holding the configuration]

# Imports
from pymongo import MongoClient
import psycopg2
import redis
import logging
import pathlib
from celery import Celery


# Class to store the config information
class Config:
    """
    Store the configuration variables for the program

    General Settings

    :param logger: The logger to use
    :type logger: logging.Logger
    :param ssl_path_type: The type of ssl path to use [Need to elaborate on this later]
    :type ssl_path_type: str

    Flask Settings

    :param secret_key: The desired secret key to use for Flask
    :type secret_key: str
    :param testing: Set if you're testing or not [Need to elaborate on this later]
    :type testing: bool
    :param debug: Set if you're debugging or not [Need to elaborate on this later]
    :type debug: bool
    :param flask_host: A host to set for Flask (0.0.0.0 is recommended for testing)
    :type flask_host: str
    :param flask_port: The port to use for Flask
    :type flask_port: int
    :param flask_ssl: Set if you're using SSL for Flask
    :type flask_ssl: bool
    :param flask_key_file: The path of the Flask SSL key file
    :type flask_key_file: pathlib.Path
    :param flask_cert_file: The path of the Flask SSL cert file
    :type flask_cert_file: pathlib.Path

    MongoDB Settings

    :param mongo_addr: The address of the MongoDB server
    :type mongo_addr: str
    :param mongo_port: The port of the MongoDB server
    :type mongo_port: int
    :param mongo_user: The MongoDB database username
    :type mongo_user: str
    :param mongo_passwd: The MongoDB database password
    :type mongo_passwd: str
    :param mongo_database: The MongoDB database name
    :type mongo_database: str
    :param mongo_ssl: The MongoDB SSL type [Need to elaborate on this later]
    :type mongo_ssl: str
    :param mongo_ca_file: The MongoDB SSL CA file path
    :type mongo_ca_file: pathlib.Path
    :param mongo_ssl_file: The MongoDB SSL file path
    :type mongo_ssl_file: pathlib.Path
    :param mongo_con: The MongoDB client
    :type mongo_con: MongoClient

    PostgresSQL Settings

    :param postgre_addr: The address of the PostgreSQL server
    :type postgre_addr: str
    :param postgre_port: The port of the PostgreSQL server
    :type postgre_port: int
    :param postgre_user: The PostgreSQL server username
    :type postgre_user: str
    :param postgre_passwd: The PostgreSQL server password
    :type postgre_passwd: str
    :param postgre_database: The PostgreSQL server database name
    :type postgre_database: str
    :param postgre_ssl: The PostgreSQL SSL type [Need to elaborate on this later]
    :type postgre_ssl: str
    :param postgre_ca_file: The PostgreSQL SSL CA file path
    :type postgre_ca_file: pathlib.Path
    :param postgre_key_file: The PostgreSQL SSL key file path
    :type postgre_key_file: pathlib.Path
    :param postgre_cert_file: The PostgreSQL SSL cert file path
    :type postgre_cert_file: pathlib.Path
    :param postgre_con: The PostgreSQL client
    :type postgre_con: psycopg2

    Redis Settings

    :param redis_addr: The address of the Redis server
    :type redis_addr: str
    :param redis_port: The port of the Redis server
    :type redis_port: int
    :param redis_user: The Redis username
    :type redis_user: str
    :param redis_passwd: The Redis password
    :type redis_passwd: str
    :param redis_database: The Redis database name
    :type redis_database: str
    :param redis_ssl: The Redis SSL type [Need to elaborate on this later]
    :type redis_ssl: str
    :param redis_ca_file: The Redis SSL CA file path
    :type redis_ca_file: pathlib.Path
    :param redis_key_file: The Redis SSL key file path
    :type redis_key_file: pathlib.Path
    :param redis_cert_file: The Redis SSL cert file path
    :type redis_cert_file: pathlib.Path
    :param redis_con: The Redis client
    :type redis_con: redis.Redis

    Celery Settings

    :param celery_redis_addr: The address of the Redis server for Celery
    :type celery_redis_addr: str
    :param celery_redis_port: The port of the Redis server for Celery
    :type celery_redis_port: int
    :param celery_redis_user: The Redis username for Celery
    :type celery_redis_user: str
    :param celery_redis_passwd: The Redis password for Celery
    :type celery_redis_passwd: str
    :param celery_redis_database: The Redis database name for Celery
    :type celery_redis_database: str
    :param celery_redis_ssl: The Redis SSL type for Celery [Need to elaborate on this later]
    :type celery_redis_ssl: str
    :param celery_redis_ca_file: The Redis SSL CA file path for Celery
    :type celery_redis_ca_file: pathlib.Path
    :param celery_redis_key_file: The Redis SSL key file path for Celery
    :type celery_redis_key_file: pathlib.Path
    :param celery_redis_cert_file: The Redis SSL cert file path for Celery
    :type celery_redis_cert_file: pathlib.Path
    :param celery_dict: The dictionary to set up Celery
    :type celery_dict: dict
    :param celery_con: The Redis client for Celery
    :type celery_con: Celery
    """
    def __init__(
        self,
        # General
        logger: logging.Logger,
        ssl_path_type: str,
        # Flask
        secret_key: str,
        testing: bool,
        debug: bool,
        flask_host: str,
        flask_port: int,
        flask_ssl: bool,
        flask_key_file: pathlib.Path,
        flask_cert_file: pathlib.Path,
        # MongoDB
        mongo_addr: str,
        mongo_port: int,
        mongo_user: str,
        mongo_passwd: str,
        mongo_database: str,
        mongo_ssl: str,
        mongo_ca_file: pathlib.Path,
        mongo_ssl_file: pathlib.Path,
        mongo_con: MongoClient,
        # PostgreSQL
        postgre_addr: str,
        postgre_port: int,
        postgre_user: str,
        postgre_passwd: str,
        postgre_database: str,
        postgre_ssl: str,
        postgre_ca_file: pathlib.Path,
        postgre_key_file: pathlib.Path,
        postgre_cert_file: pathlib.Path,
        postgre_con: psycopg2,
        # Redis
        redis_addr: str,
        redis_port: int,
        redis_user: str,
        redis_passwd: str,
        redis_database: str,
        redis_ssl: str,
        redis_ca_file: pathlib.Path,
        redis_key_file: pathlib.Path,
        redis_cert_file: pathlib.Path,
        redis_con: redis.Redis,
        # Celery
        celery_redis_addr: str,
        celery_redis_port: str,
        celery_redis_user: str,
        celery_redis_passwd: str,
        celery_redis_database: str,
        celery_redis_ssl: str,
        celery_redis_ca_file: pathlib.Path,
        celery_redis_key_file: pathlib.Path,
        celery_redis_cert_file: pathlib.Path,
        celery_dict: dict,
        celery_con: Celery,
    ):
        # General
        self.logger = logger
        self.ssl_path_type = ssl_path_type
        # Flask
        self.secret_key = secret_key
        self.testing = testing
        self.debug = debug
        self.flask_host = flask_host
        self.flask_port = flask_port
        self.flask_ssl = flask_ssl
        self.flask_key_file = flask_key_file
        self.flask_cert_file = flask_cert_file
        # MongoDB
        self.mongo_addr = mongo_addr
        self.mongo_port = mongo_port
        self.mongo_user = mongo_user
        self.mongo_passwd = mongo_passwd
        self.mongo_database = mongo_database
        self.mongo_ssl = mongo_ssl
        self.mongo_ca_file = mongo_ca_file
        self.mongo_ssl_file = mongo_ssl_file
        self.mongo_con = mongo_con
        # PostgreSQL
        self.postgre_addr = postgre_addr
        self.postgre_port = postgre_port
        self.postgre_user = postgre_user
        self.postgre_passwd = postgre_passwd
        self.postgre_database = postgre_database
        self.postgre_ssl = postgre_ssl
        self.postgre_ca_file = postgre_ca_file
        self.postgre_key_file = postgre_key_file
        self.postgre_cert_file = postgre_cert_file
        self.postgre_con = postgre_con
        # Redis
        self.redis_addr = redis_addr
        self.redis_port = redis_port
        self.redis_user = redis_user
        self.redis_passwd = redis_passwd
        self.redis_database = redis_database
        self.redis_ssl = redis_ssl
        self.redis_ca_file = redis_ca_file
        self.redis_key_file = redis_key_file
        self.redis_cert_file = redis_cert_file
        self.redis_con = redis_con
        # Celery
        self.celery_redis_addr = celery_redis_addr
        self.celery_redis_port = celery_redis_port
        self.celery_redis_user = celery_redis_user
        self.celery_redis_passwd = celery_redis_passwd
        self.celery_redis_database = celery_redis_database
        self.celery_redis_ssl = celery_redis_ssl
        self.celery_redis_ca_file = celery_redis_ca_file
        self.celery_redis_key_file = celery_redis_key_file
        self.celery_redis_cert_file = celery_redis_cert_file
        self.celery_dict = celery_dict
        self.celery_con = celery_con


# Footer Comment
# History of Contributions:
# [2024-2024] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]
