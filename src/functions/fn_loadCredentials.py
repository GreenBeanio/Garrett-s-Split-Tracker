# Header Comment
# Project: [Garrett's Split Tracker] [https://github.com/GreenBeanio/Garrett-s-Split-Tracker]
# Copyright: Copyright (c) [2024]-[2025] [Garrett's Split Tracker] Contributors
# Version: [0.1]
# Status: [Development]
# License: [MIT]
# Author(s): [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Maintainer: [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Project Description: [This project is used to track "splits" in games or activities. With the ability to display them on a livestream.]
# File Description: [A file to load the credentials into a Class Object from a JSON file]

# My Imports
from classes.cl_Config import Config
from functions.fn_validateData import validateData
from functions.fn_convertStr import convertStr
from functions.fn_convertBool import convertBool
from functions.fn_checkPath import checkPath
from functions.fn_connectMongo import connectMongo
from functions.fn_connectPostgre import connectPostgre
from functions.fn_connectRedis import connectRedis
from functions.fn_connectCelery import connectCelery

# Package Imports
import json
import pathlib
import logging
import sys

# Function to load our credentials
def loadCredentials(running_path: pathlib.Path) -> Config:
    """
    Loads the credentials into a Config Class Object from a JSON file

    I may want to switch to environment variables (or .env) to make it more practical for
    docker (or other deployment options) in the future

    :param running_path: The username to check
    :type running_path: pathlib.Path

    :return: Returns a Config Class Object
    :rtype: Config
    """
    # Create a logger
    logger = logging.getLogger("Split_Tracker")
    logger.setLevel(logging.INFO)
    # Variable for storing if there's an error
    has_error = False
    # Create the path to the settings (where the main script is running then getting the directory)
    script_path = pathlib.Path(running_path).resolve().parent.resolve()
    json_path = pathlib.Path.joinpath(script_path, "config.json")

    # Load the file if it exists
    if pathlib.Path.exists(json_path):
        with open(json_path, "r") as file:
            # Load the json
            json_obj = json.load(file)

        # Attempting to validate the data types
        for key, value in json_obj.items():
            # Getting the type of conversion based off a list
            # Strings (and paths) that need to be uppercase
            if key in [
                "SSL_PATH_TYPE",
                "MONGO_SSL",
                "POSTGRE_SSL",
                "REDIS_SSL",
                "CELERY_REDIS_SSL",
            ]:
                result, new_data = validateData(value, str, convertStr, key, logger)

            # Strings (and paths) that need to be as they are
            elif key in [
                "SECRET_KEY",
                "FLASK_HOST",
                "FLASK_KEY_FILE",
                "FLASK_CERT_FILE",
                "MONGO_ADDRESS",
                "MONGO_USER",
                "MONGO_PASS",
                "MONGO_DATABASE",
                "MONGO_CA_FILE",
                "MONGO_SSL_FILE",
                "POSTGRE_ADDRESS",
                "POSTGRE_USER",
                "POSTGRE_PASS",
                "POSTGRE_DATABASE",
                "POSTGRE_CA_FILE",
                "POSTGRE_KEY_FILE",
                "POSTGRE_CERT_FILE",
                "REDIS_ADDRESS",
                "REDIS_USER",
                "REDIS_PASS",
                "REDIS_CA_FILE",
                "REDIS_KEY_FILE",
                "REDIS_CERT_FILE",
                "CELERY_REDIS_ADDRESS",
                "CELERY_REDIS_USER",
                "CELERY_REDIS_PASS",
                "CELERY_REDIS_CA_FILE",
                "CELERY_REDIS_KEY_FILE",
                "CELERY_REDIS_CERT_FILE",
            ]:
                result, new_data = validateData(value, str, str, key, logger)

            # booleans
            elif key in ["TESTING", "DEBUG", "FLASK_SSL"]:
                # This could be problematic because any string that's not empty will be true and if empty it will be false
                result, new_data = validateData(value, bool, convertBool, key, logger)
            # integers
            elif key in [
                "FLASK_PORT",
                "MONGO_PORT",
                "POSTGRE_PORT",
                "REDIS_PORT",
                "REDIS_DATABASE",
                "CELERY_REDIS_PORT",
                "CELERY_REDIS_DATABASE",
            ]:
                result, new_data = validateData(value, int, int, key, logger)
            # If the result is true we replace the old data (even if it's the same data)
            if result:
                json_obj[key] = new_data
            # If it is not correct we acknowledge the error
            else:
                has_error = True
        # Closing if there's an error in the configuration
        if has_error:
            sys.exit()
        # Reset the error variable
        has_error = False

        # Check for valid SSL types
        check_ssl_path = False
        if json_obj["FLASK_SSL"] in [True, False]:
            if json_obj["FLASK_SSL"] == True:
                check_ssl_path = True
        else:
            logger.warning(f'Invalid option for "FLASK_SSL"! It must be true or false')
            has_error = True
        if json_obj["MONGO_SSL"] in ["NO", "PLAIN", "CERTIFICATE"]:
            if json_obj["MONGO_SSL"] == "CERTIFICATE":
                check_ssl_path = True
        else:
            logger.warning(
                f'Invalid option for "MONGO_SSL"! It must be "NO", "PLAIN", or "CERTIFICATE"'
            )
            has_error = True
        if json_obj["POSTGRE_SSL"] in [
            "NO",
            "PLAIN",
            "CA_CERTIFICATE",
            "FULL_CERTIFICATE",
        ]:
            if json_obj["POSTGRE_SSL"] in ["CA_CERTIFICATE", "FULL_CERTIFICATE"]:
                check_ssl_path = True
        else:
            logger.warning(
                f'Invalid option for "POSTGRE_SSL"! It must be "NO", "PLAIN", "CA_CERTIFICATE", or "FULL_CERTIFICATE"'
            )
            has_error = True
        if json_obj["REDIS_SSL"] in ["NO", "PLAIN", "CERTIFICATE"]:
            if json_obj["REDIS_SSL"] == "CERTIFICATE":
                check_ssl_path = True
        else:
            logger.warning(
                f'Invalid option for "REDIS_SSL"! It must be "NO", "PLAIN", or "CERTIFICATE"'
            )
            has_error = True
        if json_obj["CELERY_REDIS_SSL"] in ["NO", "PLAIN", "CERTIFICATE"]:
            if json_obj["CELERY_REDIS_SSL"] == "CERTIFICATE":
                check_ssl_path = True
        else:
            logger.warning(
                f'Invalid option for "CELERY_REDIS_SSL"! It must be "NO", "PLAIN", or "CERTIFICATE"'
            )
            has_error = True
        # Checking the SSL path type
        if check_ssl_path:
            if json_obj["SSL_PATH_TYPE"] not in ["RELATIVE", "ABSOLUTE"]:
                logger.warning(
                    f'Invalid option for "SSL_PATH_TYPE"! It must be "RELATIVE" or "ABSOLUTE"'
                )
                has_error = True
        # Closing if there's an error in the configuration
        if has_error:
            sys.exit()
        # Reset the error variable
        has_error = False

        # Setting the paths to be None for now because it's causing errors later on that
        # they're being called before their assigned.
        flask_key_path = json_obj["FLASK_KEY_FILE"]
        flask_cert_path = json_obj["FLASK_CERT_FILE"]
        mongo_ca_path = json_obj["MONGO_CA_FILE"]
        mongo_ssl_path = json_obj["MONGO_SSL_FILE"]
        postgre_ca_path = json_obj["POSTGRE_CA_FILE"]
        postgre_key_path = json_obj["POSTGRE_KEY_FILE"]
        postgre_cert_path = json_obj["POSTGRE_CERT_FILE"]
        redis_ca_path = json_obj["REDIS_CA_FILE"]
        redis_key_path = json_obj["REDIS_KEY_FILE"]
        redis_cert_path = json_obj["REDIS_CERT_FILE"]
        celery_redis_ca_path = json_obj["CELERY_REDIS_CA_FILE"]
        celery_redis_key_path = json_obj["CELERY_REDIS_KEY_FILE"]
        celery_redis_cert_path = json_obj["CELERY_REDIS_CERT_FILE"]

        # If any of the connections are using ssl and a certificate we'll check the paths
        if check_ssl_path:
            # Check for Flask
            if json_obj["FLASK_SSL"] == True:
                # If we're using relative paths
                if json_obj["SSL_PATH_TYPE"] == "RELATIVE":
                    flask_key_path = pathlib.Path.joinpath(
                        script_path, json_obj["FLASK_KEY_FILE"]
                    )
                    has_error = checkPath(flask_key_path, has_error, "FLASK_KEY_FILE")
                    flask_cert_path = pathlib.Path.joinpath(
                        script_path, json_obj["FLASK_CERT_FILE"]
                    )
                    has_error = checkPath(flask_cert_path, has_error, "FLASK_CERT_FILE")
                # If we're using absolute paths
                else:
                    flask_key_path = pathlib.Path(json_obj["FLASK_KEY_FILE"])
                    has_error = checkPath(flask_key_path, has_error, "FLASK_KEY_FILE")
                    flask_cert_path = pathlib.Path(json_obj["FLASK_CERT_FILE"])
                    has_error = checkPath(flask_cert_path, has_error, "FLASK_CERT_FILE")
            else:
                flask_key_path = json_obj["FLASK_KEY_FILE"]
                flask_cert_path = json_obj["FLASK_CERT_FILE"]
            # Check for Mongo
            if json_obj["MONGO_SSL"] == "CERTIFICATE":
                # If we're using relative paths
                if json_obj["SSL_PATH_TYPE"] == "RELATIVE":
                    mongo_ca_path = pathlib.Path.joinpath(
                        script_path, json_obj["MONGO_CA_FILE"]
                    )
                    has_error = checkPath(mongo_ca_path, has_error, "MONGO_CA_FILE")
                    mongo_ssl_path = pathlib.Path.joinpath(
                        script_path, json_obj["MONGO_SSL_FILE"]
                    )
                    has_error = checkPath(mongo_ssl_path, has_error, "MONGO_SSL_FILE")
                # If we're using absolute paths
                else:
                    mongo_ca_path = pathlib.Path(json_obj["MONGO_CA_FILE"])
                    has_error = checkPath(mongo_ca_path, has_error, "MONGO_CA_FILE")
                    mongo_ssl_path = pathlib.Path(json_obj["MONGO_SSL_FILE"])
                    has_error = checkPath(mongo_ssl_path, has_error, "MONGO_SSL_FILE")
            else:
                mongo_ca_path = json_obj["MONGO_CA_FILE"]
                mongo_ssl_path = json_obj["MONGO_SSL_FILE"]
            # Check for Postgre
            if json_obj["POSTGRE_SSL"] in ["CA_CERTIFICATE", "FULL_CERTIFICATE"]:
                # If we're using relative paths
                if json_obj["SSL_PATH_TYPE"] == "RELATIVE":
                    postgre_ca_path = pathlib.Path.joinpath(
                        script_path, json_obj["POSTGRE_CA_FILE"]
                    )
                    has_error = checkPath(postgre_ca_path, has_error, "POSTGRE_CA_FILE")
                    # If postgres is doing full verification
                    if json_obj["POSTGRE_SSL"] == "FULL_CERTIFICATE":
                        postgre_key_path = pathlib.Path.joinpath(
                            script_path, json_obj["POSTGRE_KEY_FILE"]
                        )
                        has_error = checkPath(
                            postgre_key_path, has_error, "POSTGRE_KEY_FILE"
                        )
                        postgre_cert_path = pathlib.Path.joinpath(
                            script_path, json_obj["POSTGRE_CERT_FILE"]
                        )
                        has_error = checkPath(
                            postgre_cert_path, has_error, "POSTGRE_CERT_FILE"
                        )
                # If we're using absolute paths
                else:
                    postgre_ca_path = pathlib.Path(json_obj["POSTGRE_CA_FILE"])
                    has_error = checkPath(postgre_ca_path, has_error, "POSTGRE_CA_FILE")
                    # If postgres is doing full verification
                    if json_obj["POSTGRE_SSL"] == "FULL_CERTIFICATE":
                        postgre_key_path = pathlib.Path(json_obj["POSTGRE_KEY_FILE"])
                        has_error = checkPath(
                            postgre_key_path, has_error, "POSTGRE_KEY_FILE"
                        )
                        postgre_cert_path = pathlib.Path(json_obj["POSTGRE_CERT_FILE"])
                        has_error = checkPath(
                            postgre_cert_path, has_error, "POSTGRE_CERT_FILE"
                        )
            else:
                postgre_ca_path = json_obj["POSTGRE_CA_FILE"]
                postgre_key_path = json_obj["POSTGRE_KEY_FILE"]
                postgre_cert_path = json_obj["POSTGRE_CERT_FILE"]
            # Check for Redis
            if json_obj["REDIS_SSL"] == "CERTIFICATE":
                # If we're using relative paths
                if json_obj["SSL_PATH_TYPE"] == "RELATIVE":
                    redis_ca_path = pathlib.Path.joinpath(
                        script_path, json_obj["REDIS_CA_FILE"]
                    )
                    has_error = checkPath(redis_ca_path, has_error, "REDIS_CA_FILE")
                    redis_key_path = pathlib.Path.joinpath(
                        script_path, json_obj["REDIS_KEY_FILE"]
                    )
                    has_error = checkPath(redis_key_path, has_error, "REDIS_KEY_FILE")
                    redis_cert_path = pathlib.Path.joinpath(
                        script_path, json_obj["REDIS_CERT_FILE"]
                    )
                    has_error = checkPath(redis_cert_path, has_error, "REDIS_CERT_FILE")
                # If we're using absolute paths
                else:
                    redis_ca_path = pathlib.Path(json_obj["REDIS_CA_FILE"])
                    has_error = checkPath(redis_ca_path, has_error, "REDIS_CA_FILE")
                    redis_key_path = pathlib.Path(json_obj["REDIS_KEY_FILE"])
                    has_error = checkPath(redis_key_path, has_error, "REDIS_KEY_FILE")
                    redis_cert_path = pathlib.Path(json_obj["REDIS_CERT_FILE"])
                    has_error = checkPath(redis_cert_path, has_error, "REDIS_CERT_FILE")
            else:
                redis_ca_path = json_obj["REDIS_CA_FILE"]
                redis_key_path = json_obj["REDIS_KEY_FILE"]
                redis_cert_path = json_obj["REDIS_CERT_FILE"]

            # Check for Celery
            if json_obj["CELERY_REDIS_ADDRESS"] == "CERTIFICATE":
                # If we're using relative paths
                if json_obj["SSL_PATH_TYPE"] == "RELATIVE":
                    celery_redis_ca_path = pathlib.Path.joinpath(
                        script_path, json_obj["CELERY_REDIS_CA_FILE"]
                    )
                    has_error = checkPath(
                        celery_redis_ca_path, has_error, "CELERY_REDIS_CA_FILE"
                    )
                    celery_redis_key_path = pathlib.Path.joinpath(
                        script_path, json_obj["CELERY_REDIS_KEY_FILE"]
                    )
                    has_error = checkPath(
                        celery_redis_key_path, has_error, "CELERY_REDIS_KEY_FILE"
                    )
                    celery_redis_cert_path = pathlib.Path.joinpath(
                        script_path, json_obj["CELERY_REDIS_CERT_FILE"]
                    )
                    has_error = checkPath(
                        celery_redis_cert_path, has_error, "CELERY_REDIS_CERT_FILE"
                    )
                # If we're using absolute paths
                else:
                    celery_redis_ca_path = pathlib.Path(
                        json_obj["CELERY_REDIS_CA_FILE"]
                    )
                    has_error = checkPath(
                        celery_redis_ca_path, has_error, "CELERY_REDIS_CA_FILE"
                    )
                    celery_redis_key_path = pathlib.Path(
                        json_obj["CELERY_REDIS_KEY_FILE"]
                    )
                    has_error = checkPath(
                        celery_redis_key_path, has_error, "CELERY_REDIS_KEY_FILE"
                    )
                    celery_redis_cert_path = pathlib.Path(
                        json_obj["CELERY_REDIS_CERT_FILE"]
                    )
                    has_error = checkPath(
                        celery_redis_cert_path, has_error, "CELERY_REDIS_CERT_FILE"
                    )
            else:
                celery_redis_ca_path = json_obj["CELERY_REDIS_CA_FILE"]
                celery_redis_key_path = json_obj["CELERY_REDIS_KEY_FILE"]
                celery_redis_cert_path = json_obj["CELERY_REDIS_CERT_FILE"]
        
        # Closing if there's an error in the configuration
        if has_error:
            sys.exit()
        # Reset the error variable
        has_error = False

        postgre_connection = connectPostgre(
                connection_type=json_obj["POSTGRE_SSL"],
                database=json_obj["POSTGRE_DATABASE"],
                user=json_obj["POSTGRE_USER"],
                password=json_obj["POSTGRE_PASS"],
                host=json_obj["POSTGRE_ADDRESS"],
                port=json_obj["POSTGRE_PORT"],
                sslrootcert=postgre_ca_path,
                sslcert=postgre_cert_path,
                sslkey=postgre_key_path,
            )

        # Attempting to create the database connections
        try:
            mongo_connection = connectMongo(
                connection_type=json_obj["MONGO_SSL"],
                authSource=json_obj["MONGO_DATABASE"],
                username=json_obj["MONGO_USER"],
                password=json_obj["MONGO_PASS"],
                host=json_obj["MONGO_ADDRESS"],
                port=json_obj["MONGO_PORT"],
                tlsCAFile=mongo_ca_path,
                tlsCertificateKeyFile=mongo_ssl_path,
            )
        except:
            logger.warning(
                "Invalid options for the MongoDB connection! Can't form a connection!"
            )
            has_error = True
        try:
            postgre_connection = connectPostgre(
                connection_type=json_obj["POSTGRE_SSL"],
                database=json_obj["POSTGRE_DATABASE"],
                user=json_obj["POSTGRE_USER"],
                password=json_obj["POSTGRE_PASS"],
                host=json_obj["POSTGRE_ADDRESS"],
                port=json_obj["POSTGRE_PORT"],
                sslrootcert=postgre_ca_path,
                sslcert=postgre_cert_path,
                sslkey=postgre_key_path,
            )
        except:
            logger.warning(
                "Invalid options for the PostgreSQL connection! Can't form a connection!"
            )
            has_error = True
        try:
            redis_connection = connectRedis(
                connection_type=json_obj["REDIS_SSL"],
                db=json_obj["REDIS_DATABASE"],
                username=json_obj["REDIS_USER"],
                password=json_obj["REDIS_PASS"],
                host=json_obj["REDIS_ADDRESS"],
                port=json_obj["REDIS_PORT"],
                ssl_ca_certs=redis_ca_path,
                ssl_certfile=redis_cert_path,
                ssl_keyfile=redis_key_path,
            )
        except:
            logger.warning(
                "Invalid options for the Redis connection! Can't form a connection!"
            )
            has_error = True
        try:
            # Need to test this as a connection too
            celery_dict = connectCelery(
                connection_type=json_obj["CELERY_REDIS_SSL"],
                db=json_obj["CELERY_REDIS_DATABASE"],
                username=json_obj["CELERY_REDIS_USER"],
                password=json_obj["CELERY_REDIS_PASS"],
                host=json_obj["CELERY_REDIS_ADDRESS"],
                port=json_obj["CELERY_REDIS_PORT"],
                ssl_ca_certs=celery_redis_ca_path,
                ssl_certfile=celery_redis_cert_path,
                ssl_keyfile=celery_redis_key_path,
            )
        except:
            logger.warning(
                "Invalid options for the Celery Redis connection! Can't form a connection!"
            )
            has_error = True

        # Closing if there's an error in the configuration
        if has_error:
            sys.exit()

        # Convert the json into a class
        # I'm choosing to store all the data in this class, instead of just the formed connections, in the event that
        # I need to remake the connection.
        config_class = Config(
            # General
            logger=logger,  #
            ssl_path_type=json_obj["SSL_PATH_TYPE"],  #
            # Flask
            secret_key=json_obj["SECRET_KEY"],
            testing=json_obj["TESTING"],
            debug=json_obj["DEBUG"],
            flask_host=json_obj["FLASK_HOST"],
            flask_port=json_obj["FLASK_PORT"],
            flask_ssl=json_obj["FLASK_SSL"],  #
            flask_key_file=flask_key_path,
            flask_cert_file=flask_cert_path,
            # MongoDB
            mongo_addr=json_obj["MONGO_ADDRESS"],
            mongo_port=json_obj["MONGO_PORT"],
            mongo_user=json_obj["MONGO_USER"],
            mongo_passwd=json_obj["MONGO_PASS"],
            mongo_database=json_obj["MONGO_DATABASE"],
            mongo_ssl=json_obj["MONGO_SSL"],  #
            mongo_ca_file=mongo_ca_path,
            mongo_ssl_file=mongo_ssl_path,
            mongo_con=mongo_connection,
            # PostgreSQL
            postgre_addr=json_obj["POSTGRE_ADDRESS"],
            postgre_port=json_obj["POSTGRE_PORT"],
            postgre_user=json_obj["POSTGRE_USER"],
            postgre_passwd=json_obj["POSTGRE_PASS"],
            postgre_database=json_obj["POSTGRE_DATABASE"],
            postgre_ssl=json_obj["POSTGRE_SSL"],  #
            postgre_ca_file=postgre_ca_path,
            postgre_key_file=postgre_key_path,
            postgre_cert_file=postgre_cert_path,
            postgre_con=postgre_connection,
            # Redis
            redis_addr=json_obj["REDIS_ADDRESS"],
            redis_port=json_obj["REDIS_PORT"],
            redis_user=json_obj["REDIS_USER"],
            redis_passwd=json_obj["REDIS_PASS"],
            redis_database=json_obj["REDIS_DATABASE"],
            redis_ssl=json_obj["REDIS_SSL"],  #
            redis_ca_file=redis_ca_path,
            redis_key_file=redis_key_path,
            redis_cert_file=redis_cert_path,
            redis_con=redis_connection,
            # Celery
            celery_redis_addr=json_obj["CELERY_REDIS_ADDRESS"],
            celery_redis_port=json_obj["CELERY_REDIS_PORT"],
            celery_redis_user=json_obj["CELERY_REDIS_USER"],
            celery_redis_passwd=json_obj["CELERY_REDIS_PASS"],
            celery_redis_database=json_obj["CELERY_REDIS_DATABASE"],
            celery_redis_ssl=json_obj["CELERY_REDIS_SSL"],  #
            celery_redis_ca_file=celery_redis_ca_path,
            celery_redis_key_file=celery_redis_key_path,
            celery_redis_cert_file=celery_redis_cert_path,
            celery_dict=celery_dict,
            celery_con=1,  ### Need to change this,
        )
        return config_class
    # Create a file if it doesn't exist
    else:
        default_json = {
            # General
            "SSL_PATH_TYPE": "RELATIVE_ABSOLUTE",
            # Flask
            "SECRET_KEY": "YOUR_SECRET_KEY",
            "TESTING": "TRUE_OR_FALSE",
            "DEBUG": "TRUE_OR_FALSE",
            "FLASK_HOST": "YOUR_FLASK_HOST (local machine only 127.0.0.1 or 0.0.0.0 for other machines)",
            "FLASK_PORT": "YOUR_FLASK_PORT (Default 5000)",
            "FLASK_SSL": "TRUE_OR_FALSE",  # Note that this should only be used in testing. When deploying you'll use gunicorn and nginx, or a similar stack, to serve the application.
            "FLASK_KEY_FILE": "PATH_TO_SSL_KEY",
            "FLASK_CERT_FILE": "PATH_TO_SSL_CERT",
            # Mongodb
            "MONGO_ADDRESS": "ADDRESS_TO_MONGO (local machine 127.0.0.1 or another host)",
            "MONGO_PORT": "MONGO_PORT (Default 27017)",
            "MONGO_USER": "YOUR_MONGO_USER",
            "MONGO_PASS": "YOUR_MONGO_PASSWORD",
            "MONGO_DATABASE": "MONGO_DATABASE_NAME",
            "MONGO_SSL": "NO, PLAIN, CERTIFICATE",
            "MONGO_CA_FILE": "PATH_TO_CA_FILE",
            "MONGO_SSL_FILE": "PATH_TO_SSL_FILE",
            # PostgreSQL
            "POSTGRE_ADDRESS": "ADDRESS_TO_POSTGRE (local machine 127.0.0.1 or another host)",
            "POSTGRE_PORT": "POSTGRE_PORT (Default 5432)",
            "POSTGRE_USER": "YOUR_POSTGRE_USER",
            "POSTGRE_PASS": "YOUR_POSTGRE_PASSWORD",
            "POSTGRE_DATABASE": "POSTGRE_DATABASE_NAME",
            "POSTGRE_SSL": "NO, PLAIN, CA_CERTIFICATE, FULL_CERTIFICATE",
            "POSTGRE_CA_FILE": "PATH_TO_SSL_CA",
            "POSTGRE_KEY_FILE": "PATH_TO_SSL_KEY",
            "POSTGRE_CERT_FILE": "PATH_TO_SSL_CERT",
            # Redis
            "REDIS_ADDRESS": "ADDRESS_TO_REDIS (local machine 127.0.0.1 or another host)",
            "REDIS_PORT": "REDIS_PORT (Default 6379)",
            "REDIS_USER": "YOUR_REDIS_USER",
            "REDIS_PASS": "YOUR_REDIS_PASSWORD",
            "REDIS_DATABASE": "REDIS_DATABASE_NUMBER",
            "REDIS_SSL": "NO, PLAIN, CERTIFICATE",
            "REDIS_CA_FILE": "PATH_TO_SSL_CA",
            "REDIS_KEY_FILE": "PATH_TO_SSL_KEY",
            "REDIS_CERT_FILE": "PATH_TO_SSL_CERT",
            # Celery Redis
            "CELERY_REDIS_ADDRESS": "ADDRESS_TO_CELERY_REDIS (local machine 127.0.0.1 or another host)",
            "CELERY_REDIS_PORT": "CELERY_REDIS_PORT (Default 6379)",
            "CELERY_REDIS_USER": "YOUR_CELERY_REDIS_USER",
            "CELERY_REDIS_PASS": "YOUR_CELERY_REDIS_PASSWORD",
            "CELERY_REDIS_DATABASE": "CELERY_REDIS_DATABASE_NUMBER",
            "CELERY_REDIS_SSL": "NO, PLAIN, CERTIFICATE",
            "CELERY_REDIS_CA_FILE": "PATH_TO_SSL_CA",
            "CELERY_REDIS_KEY_FILE": "PATH_TO_SSL_KEY",
            "CELERY_REDIS_CERT_FILE": "PATH_TO_SSL_CERT",
        }
        with open(json_path, "w+") as file:
            json_obj = json.dumps(default_json, indent=4, sort_keys=False, default=str)
            file.write(json_obj)
        # Maybe not the bes idea, but it is what it is
        sys.exit("Fill in the config file")

# Footer Comment
# History of Contributions:
# [2024-2025] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]