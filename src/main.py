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

# Import Credentials
from stored_credentials import app_config

# Import the Flask App
from app import flask_app

# Show the blueprint (URL in general) map
# print(flask_app.url_map)

# Start the flask app
if __name__ == "__main__":
    # If we're using SSL with Flask (Only use this for testing! On deployment do it through Gunicorn and Nginx)
    if app_config.flask_ssl:
        flask_app.run(
            host=app_config.flask_host,
            port=app_config.flask_port,
            debug=app_config.debug,
            ssl_context=(app_config.flask_cert_file, app_config.flask_key_file),
        )
    # Run Flask without SSL
    else:
        flask_app.run(
            host=app_config.flask_host,
            port=app_config.flask_port,
            debug=app_config.debug,
        )

# Then use these cli commands (running flask first seems to matter, but the order of these 2 doesn't really,
# but I start the beat first because the worker needs it):
# "celery -A make_celery beat --loglevel INFO"
# "celery -A make_celery worker --loglevel INFO"


# Footer Comment
# History of Contributions:
# [2024-2024] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]
