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
        mongo_port: str,
        mongo_user: str,
        mongo_passwd: str,
        mongo_database: str,
        mongo_ssl: str,
        mongo_ca_file: pathlib.Path,
        mongo_ssl_file: pathlib.Path,
        mongo_con: MongoClient,
        # PostgreSQL
        postgre_addr: str,
        postgre_port: str,
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
        redis_port: str,
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
