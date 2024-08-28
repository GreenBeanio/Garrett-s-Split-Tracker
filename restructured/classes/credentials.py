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


# Class to store the config information
class Config:
    def __init__(
        self,
        secret_key: str,
        testing: bool,
        mongo_addr: str,
        mongo_user: str,
        mongo_passwd: str,
        mongo_port: str,
        mongo_con: MongoClient,
        redis_addr: str,
        redis_port: str,
        redis_passwd: str,
        celery_dict: dict,
    ):
        self.secret_key = secret_key
        self.testing = testing
        self.mongo_addr = mongo_addr
        self.user = mongo_user
        self.passwd = mongo_passwd
        self.mongo_port = mongo_port
        self.mongo_con = mongo_con
        self.redis_addr = redis_addr
        self.redis_port = redis_port
        self.redis_passwd = redis_passwd
        self.celery_dict = celery_dict


# Footer Comment
# History of Contributions:
# [2024-2024] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]
