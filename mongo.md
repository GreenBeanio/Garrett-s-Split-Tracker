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
