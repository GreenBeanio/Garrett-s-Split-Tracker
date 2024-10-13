# Header Comment
# Project: [Garrett's Split Tracker] [https://github.com/GreenBeanio/Garrett-s-Split-Tracker]
# Copyright: Copyright (c) [2024]-[2024] [Garrett's Split Tracker] Contributors
# Version: [0.1]
# Status: [Development]
# License: [MIT]
# Author(s): [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Maintainer: [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
# Project Description: [This project is used to track "splits" in games or activities. With the ability to display them on a livestream.]
# File Description: [Loads the credentials]

# My Imports
from classes.credentials import Config

# My Imports for celery beats
# import auth.functions.auth_functions

# Imports
import json
import pathlib
import sys
from pymongo import MongoClient
import datetime
import psycopg2
import redis
import ssl
import logging
import sys
from typing import Union


# Function to check if a path exists
def checkPath(
    path: pathlib.Path, has_error: bool, variable: str, log: logging.Logger
) -> bool:
    # If the path exists return a result based off the existing has_error
    if pathlib.Path.exists(path):
        return has_error
    # If the path doesn't exist return an error
    else:
        log.warning(f'Invalid path for "{variable}"')
        return True


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
            tsl=True,
        )
    # If there's SSL with Certificates
    elif connection_type == "CERTIFICATE":
        mongo_client = MongoClient(
            authSource=authSource,
            username=username,
            password=password,
            host=host,
            port=port,
            tsl=True,
            tlsCAFile=tlsCAFile,
            tlsCertificateKeyFile=tlsCertificateKeyFile,
        )
    # print(f'mongodb://{json_obj["MONGO_USER"]}:{json_obj["MONGO_PASS"]}@{json_obj["MONGO_ADDRESS"]}:{json_obj["MONGO_PORT"]}/?authSource={json_obj["MONGO_DATABASE"]}&tls=true&tlsCAFILE={json_obj["MONGO_SSL_FILE"]}')
    # print(f'mongodb://{json_obj["MONGO_USER"]}:{json_obj["MONGO_PASS"]}@{json_obj["MONGO_ADDRESS"]}:{json_obj["MONGO_PORT"]}/?authSource={json_obj["MONGO_DATABASE"]}')
    # print(mongo_client)
    # print(mongo_client.server_info())
    # Return the resulting connection
    return mongo_client


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
    # If there's no SSL
    if connection_type == "NO":
        # Create the celery dict
        redis_uri = f"redis://{username}:{password}@{host}:{port}/{db}"
        celery_dict = dict(
            broker_url=redis_uri,
            result_backend=redis_uri,
            task_ignore_result=True,
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


# Function to load our credentials
def loadCredentials(running_path: pathlib.Path) -> Config:
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

        # Check for valid SSL types
        check_ssl_path = False
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
        # Checking the SSL path
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

        # If any of out connections are using ssl and a certificate we'll check the paths
        if check_ssl_path:
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
            # Check for Postgre
            if json_obj["POSTGRE_SSL"] in ["CA_CERTIFICATE", "FULL_CERTIFICATE"]:
                # If we're using relative paths
                if json_obj["SSL_PATH_TYPE"] == "RELATIVE":
                    postgre_ca_path = pathlib.Path.joinpath(
                        script_path, json_obj["POSTGRE_CA_FILE"]
                    )
                    has_error = checkPath(postgre_ca_path, has_error, "POSTGRE_CA_FILE")
                    # If postgres is doing full verificaiton
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
                    # If postgres is doing full verificaiton
                    if json_obj["POSTGRE_SSL"] == "FULL_CERTIFICATE":
                        postgre_key_path = pathlib.Path(json_obj["POSTGRE_KEY_FILE"])
                        has_error = checkPath(
                            postgre_key_path, has_error, "POSTGRE_KEY_FILE"
                        )
                        postgre_cert_path = pathlib.Path(json_obj["POSTGRE_CERT_FILE"])
                        has_error = checkPath(
                            postgre_cert_path, has_error, "POSTGRE_CERT_FILE"
                        )
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
        # Closing if there's an error in the configuration
        if has_error:
            sys.exit()
        # Reset the error variable
        has_error = False

        ### STOPPED HERE ###
        # Need to replace the below to use the functions and do exception handling to quit if one of them doesn't connect
        # Also need to see if I can test the celery connection since I didn't do that in here before.
        # Also should probably make a shell script to start the flask program, celery worker, and celery beat with one command
        ### STOPPED HERE ###

        # Connect to MongoDB
        if json_obj["MONGO_SSL"]:
            # print(f'mongodb://{json_obj["MONGO_USER"]}:{json_obj["MONGO_PASS"]}@{json_obj["MONGO_ADDRESS"]}:{json_obj["MONGO_PORT"]}/?authSource={json_obj["MONGO_DATABASE"]}&tls=true&tlsCAFILE={json_obj["MONGO_SSL_FILE"]}')
            mongo_client = MongoClient(
                authSource=json_obj["MONGO_DATABASE"],
                username=json_obj["MONGO_USER"],
                password=json_obj["MONGO_PASS"],
                host=json_obj["MONGO_ADDRESS"],
                port=json_obj["MONGO_PORT"],
                # authMechanism="SCRAM-SHA-256",
                tsl=True,
                tlsCAFile=json_obj["MONGO_SSL_FILE"],
                # tlsCertificateKeyFile=json_obj["MONGO_SSL_FILE"] # Might need to try this one instead if that one doesn't work
            )
        else:
            # print(f'mongodb://{json_obj["MONGO_USER"]}:{json_obj["MONGO_PASS"]}@{json_obj["MONGO_ADDRESS"]}:{json_obj["MONGO_PORT"]}/?authSource={json_obj["MONGO_DATABASE"]}')
            # Create a mongoDB connection
            mongo_client = MongoClient(
                f'mongodb://{json_obj["MONGO_USER"]}:{json_obj["MONGO_PASS"]}@{json_obj["MONGO_ADDRESS"]}:{json_obj["MONGO_PORT"]}/?authSource={json_obj["MONGO_DATABASE"]}'
            )
            # print(mongo_client)
            # print(mongo_client.server_info())

        # Connect to PostgreSQL
        if json_obj["POSTGRE_SSL"]:
            ## Create the postgres client
            postgre_client = psycopg2.connect(
                database=json_obj["POSTGRE_DATABASE"],
                user=json_obj["POSTGRE_USER"],
                password=json_obj["POSTGRE_PASS"],
                host=json_obj["POSTGRE_ADDRESS"],
                port=json_obj["POSTGRE_PORT"],
                sslmode="verify-full",  # "require" or "verify-ca"
                # For verify-ca and verify-full
                sslrootcert=json_obj["POSTGRE_CA_FILE"],
                # For verify-full
                sslcert=json_obj["POSTGRE_CERT_FILE"],
                sslkey=json_obj["POSTGRE_KEY_FILE"],
            )
        else:
            ## Create the postgres client
            postgre_client = psycopg2.connect(
                database=json_obj["POSTGRE_DATABASE"],
                user=json_obj["POSTGRE_USER"],
                password=json_obj["POSTGRE_PASS"],
                host=json_obj["POSTGRE_ADDRESS"],
                port=json_obj["POSTGRE_PORT"],
            )

        # Connect to Redis
        if json_obj["REDIS_SSL"]:
            # Create the celery dict
            celery_dict = dict(
                broker_url=f'redis://ANY_USERNAME:{json_obj["REDIS_PASS"]}@{json_obj["REDIS_ADDRESS"]}:{json_obj["REDIS_PORT"]}',
                result_backend=f'redis://ANY_USERNAME:{json_obj["REDIS_PASS"]}@{json_obj["REDIS_ADDRESS"]}:{json_obj["REDIS_PORT"]}',
                task_ignore_result=True,
                # Beat schedule for timing repetitive events (You can set up the schedules in here like this too instead of with the functions)
                # "task-name" : {"task": "function", "schedule": time_in_seconds}
                # beat_schedule={
                #     "task-every-minute": {
                #         "task": "auth.functions.auth_functions.removeExpiredSessions",
                #         "schedule": datetime.timedelta(seconds=1),
                #     }
                # },
                broker_use_ssl={
                    "keyfile": json_obj["REDIS_KEY_FILE"],
                    "certfile": json_obj["REDIS_CERT_FILE"],
                    "ca_certs": json_obj["REDIS_CA_FILE"],
                    "cert_reqs": ssl.CERT_REQUIRED,
                },
            )
            # Creating redis connection
            redis_client = redis.Redis(
                host=json_obj["REDIS_ADDRESS"],
                port=json_obj["REDIS_PORT"],
                password=json_obj["REDIS_PASS"],
                ssl=True,
                ssl_certfile=json_obj["REDIS_CERT_FILE"],
                ssl_keyfile=json_obj["REDIS_KEY_FILE"],
                ssl_ca_certs=json_obj["REDIS_CA_FILE"],
            )
        else:
            # Create the celery dict
            celery_dict = dict(
                broker_url=f'redis://ANY_USERNAME:{json_obj["REDIS_PASS"]}@{json_obj["REDIS_ADDRESS"]}:{json_obj["REDIS_PORT"]}',
                result_backend=f'redis://ANY_USERNAME:{json_obj["REDIS_PASS"]}@{json_obj["REDIS_ADDRESS"]}:{json_obj["REDIS_PORT"]}',
                task_ignore_result=True,
                # Beat schedule for timing repetitive events (You can set up the schedules in here like this too instead of with the functions)
                # "task-name" : {"task": "function", "schedule": time_in_seconds}
                # beat_schedule={
                #     "task-every-minute": {
                #         "task": "auth.functions.auth_functions.removeExpiredSessions",
                #         "schedule": datetime.timedelta(seconds=1),
                #     }
                # },
            )
            # Creating redis connection
            redis_client = redis.Redis(
                host=json_obj["REDIS_ADDRESS"],
                port=json_obj["REDIS_PORT"],
                password=json_obj["REDIS_PASS"],
            )

        # Convert the json into a class (why not, probably better than a dictionary)
        # Putting the mongodb connection in here may be very foolish. I might want to just connect multiple times.
        config_class = Config(
            # Secret key for flask
            secret_key=json_obj["SECRET_KEY"],
            testing=json_obj["TESTING"],
            debug=json_obj["DEBUG"],
            flask_host=json_obj["FLASK_HOST"],
            flask_port=json_obj["FLASK_PORT"],
            # Mongo config
            mongo_addr=json_obj["MONGO_ADDRESS"],
            mongo_port=json_obj["MONGO_PORT"],
            mongo_user=json_obj["MONGO_USER"],
            mongo_passwd=json_obj["MONGO_PASS"],
            mongo_database=json_obj["MONGO_DATABASE"],
            mongo_ssl=json_obj["MONGO_SSL"],
            mongo_key=json_obj["MONGO_SSL_FILE"],
            mongo_con=mongo_client,
            # Postgres config
            postgre_addr=json_obj["POSTGRE_ADDRESS"],
            postgre_port=json_obj["POSTGRE_PORT"],
            postgre_user=json_obj["POSTGRE_USER"],
            postgre_passwd=json_obj["POSTGRE_PASS"],
            postgre_database=json_obj["POSTGRE_DATABASE"],
            postgre_ssl=json_obj["POSTGRE_SSL"],
            postgre_key=json_obj["POSTGRE_KEY_FILE"],
            postgre_cert=json_obj["POSTGRE_CERT_FILE"],
            postgre_ca=json_obj["POSTGRE_CA_FILE"],
            postgre_con=postgre_client,
            # Celery/Redis config
            redis_addr=json_obj["REDIS_ADDRESS"],
            redis_port=json_obj["REDIS_PORT"],
            redis_passwd=json_obj["REDIS_PASS"],
            redis_ssl=json_obj["REDIS_SSL"],
            redis_key=json_obj["REDIS_KEY_FILE"],
            redis_cert=json_obj["REDIS_CERT_FILE"],
            redis_ca=json_obj["REDIS_CA_FILE"],
            redis_con=redis_client,
            celery_dict=celery_dict,
            # I don't even really need to store the password, address, and user name if I only make the connection here. We'll see if I change that later.
        )
        # print(auth.functions.auth_functions.removeExpiredSessions.name)  # TEMP: Checking celery
        return config_class
    # Create a file if it doesn't exist
    else:
        default_json = {
            # Flask
            "SECRET_KEY": "YOUR_SECRET_KEY",
            "TESTING": "TRUE_OR_FALSE",
            "DEBUG": "TRUE_OR_FALSE",
            "FLASK_HOST": "YOUR_FLASK_HOST (local machine only 127.0.0.1 or 0.0.0.0 for other machines)",
            "FLASK_PORT": "YOUR_FLASK_PORT (Default 5000)",
            # General
            "SSL_PATH_TYPE": "RELATIVE_ABSOLUTE",
            # Mongodb
            "MONGO_ADDRESS": "ADDRESS_TO_MONGO (local machine 127.0.0.1 or another host)",
            "MONGO_PORT": "MONGO_PORT (Default 27017)",
            "MONGO_USER": "YOUR_MONGO_USER",
            "MONGO_PASS": "YOUR_MONGO_PASSWORD",
            "MONGO_DATABASE": "MONGO_DATABASE_NAME",
            "MONGO_SSL": "NO, PLAIN, CERTIFICATE",  ###
            "MONGO_CA_FILE": "PATH_TO_CA_FILE",  ####
            "MONGO_SSL_FILE": "PATH_TO_SSL_FILE",
            # PostgreSQL
            "POSTGRE_ADDRESS": "ADDRESS_TO_POSTGRE (local machine 127.0.0.1 or another host)",
            "POSTGRE_PORT": "POSTGRE_PORT (Default 5432)",
            "POSTGRE_USER": "YOUR_POSTGRE_USER",
            "POSTGRE_PASS": "YOUR_POSTGRE_PASSWORD",
            "POSTGRE_DATABASE": "POSTGRE_DATABASE_NAME",
            "POSTGRE_SSL": "NO, PLAIN, CA_CERTIFICATE, FULL_CERTIFICATE",  ###
            "POSTGRE_CA_FILE": "PATH_TO_SSL_CA",
            "POSTGRE_KEY_FILE": "PATH_TO_SSL_KEY",
            "POSTGRE_CERT_FILE": "PATH_TO_SSL_CERT",
            # Redis
            "REDIS_ADDRESS": "ADDRESS_TO_REDIS (local machine 127.0.0.1 or another host)",
            "REDIS_PORT": "REDIS_PORT (Default 6379)",
            "REDIS_USER": "YOUR_REDIS_USER",
            "REDIS_PASS": "YOUR_REDIS_PASSWORD",  ###
            "REDIS_DATABASE": "REDIS_DATABASE_NUMBER",  ###
            "REDIS_SSL": "NO, PLAIN, CERTIFICATE",  ###
            "REDIS_CA_FILE": "PATH_TO_SSL_CA",
            "REDIS_KEY_FILE": "PATH_TO_SSL_KEY",
            "REDIS_CERT_FILE": "PATH_TO_SSL_CERT",
            # Celery Redis
            "CELERY_REDIS_ADDRESS": "ADDRESS_TO_CELERY_REDIS (local machine 127.0.0.1 or another host)",
            "CELERY_REDIS_PORT": "CELERY_REDIS_PORT (Default 6379)",
            "CELERY_REDIS_USER": "YOUR_CELERY_REDIS_USER",
            "CELERY_REDIS_PASS": "YOUR_CELERY_REDIS_PASSWORD",  ###
            "CELERY_REDIS_DATABASE": "CELERY_REDIS_DATABASE_NUMBER",  ###
            "CELERY_REDIS_SSL": "NO, PLAIN, CERTIFICATE",  ###
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
# [2024-2024] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document]
