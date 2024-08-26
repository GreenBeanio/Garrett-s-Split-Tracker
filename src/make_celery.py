# Header Comment
# Project: [Garrett's Split Tracker] [https://github.com/GreenBeanio/Garrett-s-Split-Tracker]
# Copyright: Copyright (c) [2024]-[2024] [Garrett's Split Tracker] Contributors
# Version: [0.1]
# Status: [Development]
# License: [MIT]
# Author(s): [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Maintainer: [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Project Description: [This project is used to track "splits" in games or activities. With the ability to display them on a livestream.]
# File Description: [Creates the flask and celery apps.]

from py.create_apps import createFlaskApp
from py.functions import loadCredentials

# Load credentials
cred = loadCredentials(__file__)

# # Test redis
# from redis import Redis

# r = Redis.from_url(
#     f"redis://ANY_USERNAME:{cred.redis_passwd}@{cred.redis_addr}:{cred.redis_port}"
# )
# print(r.ping())

flask_app = createFlaskApp(__name__, cred)
celery_app = flask_app.extensions["celery"]

# Footer Comment
# History of Contributions:
# [2024-2024] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]
