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

- I'm using WSL to run my python. I have to change the bindIP in the MongoDB config file from 127.0.0.1 to 0.0.0.0.
- Then I need to make sure there is a firewall rule to allow inbound data from TCP port 27017 (Mongo port)
  - New-NetFirewallRule -DisplayName "MongoDB from WSL2" -InterfaceAlias "vEthernet (WSL)" -Direction Inbound -Protocol TCP -LocalPort 27017 -Action Allow
- Then I need to set the ip to be used for mongo to the ip address found by running "ipconfig" in powershell and getting the ipv4 address for the WSL ethernet adapter.

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

I am running redis on WSL as well (it supports wsl but MongoDB doesn't) so I can just use localhost as the address still.

# Celery
Celery is a despicable module.

- I'm using WSL to run my python. I have to change the bindIP in the MongoDB config file from 127.0.0.1 to 0.0.0.0.
- Then I need to make sure there is a firewall rule to allow inbound data from TCP port 27017 (Mongo port)
  - New-NetFirewallRule -DisplayName "MongoDB from WSL2" -InterfaceAlias "vEthernet (WSL)" -Direction Inbound -Protocol TCP -LocalPort 27017 -Action Allow
- Then I need to set the ip to be used for mongo to the ip address found by running "ipconfig" in powershell and getting the ipv4 address for the WSL ethernet adapter.
