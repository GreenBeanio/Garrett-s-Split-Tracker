# MongoDB

create database

```use split_tracker;```

create a table/collection

```db.createCollection("users");```
```db.createCollection("sessions");```

create a user

```
db.createUser ({
    user: "MONGO_USER",
    pwd: "MONGO_PASS",
    roles : [ {role : "readWrite", db: "split_tracker"} ]
});
```

# Redis

stop redis
```sudo service redis-server stop```

Open the configuration file
```/etc/redis/redis.conf```
Then find
```# requirepass foobared```
Uncomment it and change it to your password

start redis
```sudo service redis-server start```

Check if there's a password

```
redis-cli
config get requirepass
```

Test the password

```
AUTH yourpassword

You could also try
```config set requirepass yourpassword```
but it seems to not be persistent when redis restarts

# Celery
Celery is a despicable module.
