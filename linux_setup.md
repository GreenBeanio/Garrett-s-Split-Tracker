# Notes on Setting up Linux

Assuming using Ubuntu 22.04.1 LTS jammy

## Setting up basics

Maybe add notes on setting up the basic linux stuff like disabling passwords and enabling ssh keys and stuff later. Creating ssh key to connect to it from your client and stuff too.

## Setting up group

- Creating the group
  - sudo groupadd databases

## Creating a user to access this project (for backups and stuff)

- Create the user
  - sudo useradd -m -d /home/projects -s /bin/bash split_tracker
- Add a password to the user
  - sudo passwd split_tracker
- Create the ssh directory
  - sudo mkdir /home/projects/.ssh
- Copy the ssh key in
  - sudo touch /home/projects/.ssh/authorized_keys
    - Put the public keys into the file (however you want. Here are some options)
      - curl file_somewhere >> /home/projects/.ssh/authorized_keys
      - Vim /home/projects/.ssh/authorized_keys
- Set the directory permissions
  - sudo chown -R split_tracker:split_tracker /home/projects/.ssh
  - sudo chmod 700 /home/projects/.ssh
  - sudo chmod 600 /home/projects/.ssh/authorized_keys
- Add a group
  - sudo usermod -a -G databases split_tracker

## Creating a directory to store files for this project

- Switch to the split_tracker user
  - sudo -u split_tracker

- Create the directory
  - sudo mkdir /projects
  - cd /projects
- Creating the directory for SSL
  - sudo mkdir ssl
- Creating a directory for storing links to config files
  - sudo mkdir configs

- Changing the ownership and permissions
  - Change the ownership
    - sudo chown -R split_tracker:databases /projects
  - Change the permissions
    - sudo chmod -R u=rwx,g=rwx,o=rx /projects

- Exit the user
  - exit

- XXX I will need to add the actual contents of this repo in here too

## DynamicDNS

If you're hosting this from your home server (that probably has a dynamic IP) and not a VPS (which probably has a static IP) you will probably want to set up Dynamic DNS with your domain (assuming that you're using a domain and not an IP address).

I currently use NameCheap for my domains and you can use dynamic DNS with them through ddclient.

- Install ddclient
  - sudo apt-get install ddclient
- Go into the configuration file
  - sudo vim /etc/ddclient.conf
  - The information in the domain should look something like this
    - <pre><code>
        #NameCheap
        daemon=300
        ssl=yes
        use=web
        web=dynamicdns.park-your-domain.com/getip
        protocol=namecheap
        server=dynamicdns.park-your-domain.com
        # Your Domain
        login=your.domain
        password='Your DNS Password From Namecheap'
        host.your.domain</code></pre>
    - You will most likely need a @.you.domain as one of the domains for the root domain dns record.
  - Test the script
    - sudo ddclient -daemon=0 -noquiet -debug
  - Set up a daemon
    - sudo vim /etc/default/ddclient
    - Set or add the following
      - <pre><code>
        run_daemon="true"
        daemon_interval="300"</code></pre>
    - systemctl restart ddclient
    - systemctl status ddclient
- In the configuration file you will need to add all the subdomains you're using on different lines.
- You will need to add the following A records in your domain registrar from that domain and subdomain to the ip.
  - With NameCheap I believe the ip address you enter shouldn't matter because the dynamic DNS will update it automatically.

## Creating the SSL (Using LetsEncrypt)

- Install packages
  - sudo apt update
  - sudo apt install python3 python3-venv libaugeas0
- Install Certbot to use LetsEncrypt
  - If you have installed it through apt or somewhere else before remove it first
    - sudo apt-get remove certbot
    - sudo apt purge
    - sudo apt autoremove
  - Install Certbot
    - sudo python3 -m venv /opt/certbot/
    - sudo /opt/certbot/bin/pip install --upgrade pip
    - sudo /opt/certbot/bin/pip install certbot
    - sudo ln -s /opt/certbot/bin/certbot /usr/bin/certbot
    - Depending on if your web server is currently running
      - If it isn running
        - sudo certbot certonly --standalone
      - If it isn't running
        - sudo certbot certonly --webroot
      - Using certonly because I don't want to install it into a web server yet (nginx specifically)
      - I would recommend turning off any web servers currently running on port 80 and running standalone mode for now.
        - sudo systemctl stop nginx.service
        - Then run the following when all of this step has been completed
          - sudo systemctl start nginx.service
      - Because I want to save the ssl files to a specific location I ran
        - sudo certbot certonly --standalone --config-dir /projects/ssl
      - If you want to specify a domain without any prompts from certbot do (you can have multiple -d arguments for multiple domains)
        - sudo certbot certonly --standalone -d subdomain.domain.topleveldomain
        - or if using the custom directory
          - sudo certbot certonly --standalone --config-dir /projects/ssl -d subdomain.domain.topleveldomain
      - Now if you want to use a wildcard subdomain instead of individual subdomains it's more complicated
        - ```sudo certbot certonly --manual --server https://acme-v02.api.letsencrypt.org/directory --preferred-challenges dns -d *.domain.topleveldomain```
        - or if using the custom directory
          - ```sudo certbot certonly --manual --config-dir /projects/ssl --server https://acme-v02.api.letsencrypt.org/directory --preferred-challenges dns -d *.domain.topleveldomain```
        - Then go to your domain name provider and add a txt record using the host it gives you and the value it gives you.
          - For Namecheap we make the host "_acme-challenge" or whatever it tells you without the rest of the domain.
          - The value will be what it gives you.
        - Before continuing check that the new record has been deployed. It should provide a link to google admin toolbox to check the records on your domain. If not you can go to <https://toolbox.googleapps.com/apps/dig> and put in the host.your.domain that you just put into your domain name registrar and selecting txt.
        - When it is posted you can press enter to continue. However, it seems that this wildcard wont be renewed automatically like the specific subdomains will. You will have to do this command again when it expires (before it expires preferably). You can also remove the txt record from the DNS.
          - I could be wrong about it not renewing automatically, but it says that. I will see when my test expires in the future.
      - I don't want to use a wildcard for this project, because I only have static subdomains. The subdomains this project uses is:
        - ```mongo.youredomain.xxx```
        - ```postgre.youredomain.xxx```
        - ```redis.youredomain.xxx```
        - ```www.youredomain.xxx```
        - ```youredomain.xxx```
      - Realistically you don't actually even need to do the mongo, postgre, and redis subdomains if they're all running locally on one machine or on a local network, you also wouldn't even need to set up ssl for them. However, while developing this I am using a separate server for the databases and my local machine for running the program. It's still on a local network though which negates the need for all of this ssl and domain actions, but it's a good learning experience to experiment with it. If you're running everything locally you can feel free to ignore everything involving ssl on the databases and their subdomains. However, you should still set up www and the base domain with ssl because you're going to need HTTPS if you're not a goober.
      - Also note that if using dynamic dns through ddclient you will need to add all the subdomains in there too.
    - Set up automatic renewal
      - <pre><code>echo "0 0,12 ** *root /opt/certbot/bin/python -c 'import random; import time; time.sleep(random.random()* 3600)' && sudo certbot renew -q" | sudo tee -a /etc/crontab > /dev/null</code></pre>
      - Since I want to use a different directory than default I did
        - <pre><code>echo "0 0,12 ** *root /opt/certbot/bin/python -c 'import random; import time; time.sleep(random.random()* 3600)' && sudo certbot renew --config-dir /projects/ssl -q" | sudo tee -a /etc/crontab > /dev/null<code></pre>
    - Manually renew certificates
      - sudo certbot renew -q
      - If using the custom location it's
        - sudo certbot renew --config-dir /projects/ssl -q
    - If you ever need to update certbot run
      - sudo /opt/certbot/bin/pip install --upgrade certbot
    - You can view certificates with this command
      - certbot certificates
      - If using the custom location it's
        - certbot certificates --config-dir /projects/ssl
    - Note that instead of using the config-dir for a custom location you could also use "sudo ln -s /etc/letsencrypt/live/ /projects/ssl" to create a symbolic link to all the files, but I'm choosing to use the config-dir approach.
    - You can also add the argument flag "--register-unsafely-without-email" to any of the certbot commands to not use an email.
    - Run this to make it accessible. (Not sure if this will become a problem later, but we need to be able to access it)
      - sudo chmod -R u=rwx,g=rwx,o=rx /projects/ssl
      - sudo chown split_tracker:databases /projects/ssl
    - Notes:
      - Certbot will return 4 files:
        - cert.pem
          - The public key. However, this one shouldn't be used with most software.
        - chain.pem
          - The certificate chain.
        - fullchain.pem
          - The certificate that you will use in most server software. It is a combination of the cert.pem and the chain.pem
        - privkey.pem
          - The private key

## Installing PostgreSQL

### Creating a new user

- Create the user
  - sudo useradd -m -d /home/u_postgres -s /bin/bash u_postgres
- Add a password to the user
  - sudo passwd u_postgres
- Create the ssh directory
  - sudo mkdir /home/u_postgres/.ssh
- Copy the ssh key in
  - sudo touch /home/u_postgres/.ssh/authorized_keys
    - Put the public keys into the file (however you want. Here are some options)
      - curl file_somewhere >> /home/u_postgres/.ssh/authorized_keys
      - Vim /home/u_postgres/.ssh/authorized_keys
- Set the directory permissions
  - sudo chown -R u_postgres:u_postgres /home/u_postgres/.ssh
  - sudo chmod 700 /home/u_postgres/.ssh
  - sudo chmod 600 /home/u_postgres/.ssh/authorized_keys
- Add a group
  - sudo usermod -a -G databases u_postgres

### Installing

- Install
  - sudo apt install postgresql

### Creating a link to the config file

- Create the directory
  - sudo mkdir /projects/configs/postgres
- Edit the ownership and permission
  - sudo chmod u=rwx,g=rwx,o=rx /projects/configs/postgres
  - sudo chown split_tracker:databases /projects/configs/postgres
- Create the soft link
  - sudo ln -s /etc/postgresql/version#/main/postgresql.conf /projects/configs/postgres/postgresql.conf
  - sudo ln -s /etc/postgresql/version#/main/pg_hba.conf /projects/configs/postgres/pg_hba.conf

### Changing the data path

- Start postgresql
  - sudo systemctl start postgresql
- Enter postgresql and get the current directory
  - sudo -u postgres psql
  - SHOW data_directory;
    - Copy this path. It will most likely be like this "/var/lib/postgresql/version#/main".
  - exit
- Stop postgresql
  - sudo systemctl stop postgresql
- Copy the original data to your new location
  - sudo rsync -a /var/lib/postgresql/version#/main /projects/
  - sudo mv /projects/main /projects/postgres
- Change the group owner and permissions of the files because we want to be able to access it
  - sudo chown postgres:databases /projects/postgres
  - sudo chmod u=rwx,g=rx,o= /projects/postgres
- Change the default path
  - sudo vim /etc/postgresql/version#/main/postgresql.conf
  - Change the data_directory option to the path
- Check that postgres launches
  - sudo systemctl start postgresql
  - sudo systemctl status postgresql
    - If it's active then good. If not check the path you entered.
  - sudo systemctl stop postgresql

### Adding SSL

- Go into the configuration file
  - sudo vim /etc/postgresql/version#/main/postgresql.conf
  - Find and modify, or add, the following. You will need to change the path to match the domain name you used. You can find it by running "sudo ls /projects/ssl/live/"
    - <pre><code>
    ssl = on
    #ssl_ca_file = '/projects/ssl/live/youredomain.xxx/chain.pem'
    #ssl_cert_file = '/projects/ssl/live/youredomain.xxx/cert.pem'
    ssl_cert_file = '/projects/ssl/live/youredomain.xxx/fullchain.pem'
    ssl_key_file = '/projects/ssl/live/youredomain.xxx/privkey.pem'
    ssl_ciphers = 'HIGH:MEDIUM:+3DES:!aNULL'
    ssl_prefer_server_ciphers = on
    </code></pre>
- Add rule to allow for ssl
  - sudo vim /etc/postgresql/version#/main/pg_hba.conf
  - Add the following to the end
    - <pre><code>
    hostssl  all         all          0.0.0.0/0      md5
    </code></pre>
- Test that it works
  - sudo systemctl start postgresql
  - sudo systemctl status postgresql
    - If it's active then good. If not check the paths you entered.
  - sudo systemctl stop postgresql

### Setting up

The configuration file can be found at "/etc/postgresql/\*/main/postgresql.conf" if needed (the \* is your version of postgreSQL)

- Add the created user to the group
  - sudo usermod -a -G databases postgres

- Systemd Approach (what you'll likely use)
  - File location is at one of these
    - /lib/systemd/system/postgresql.service
    - /etc/systemd/system/postgresql.service
  - Start the service
  - sudo systemctl start postgresql
  - Check the status
  - sudo systemctl status postgresql
  - Enable it on boot
  - sudo systemctl enable postgresql

- Stuff from the documentation (other method)
  - Starting the database with a data directory
  - In the background
    - postgres -D /usr/local/pgsql/data >logfile 2>&1 &
  - Active
    - postgres -D /usr/local/pgsql/data
  - With wrapper
    - pg_ctl start -l logfile
  - With user
    - su postgres -c 'pg_ctl start -D /usr/local/pgsql/data -l serverlog'

- To use the shell
  - sudo -u postgres psql

## Installing MongoDB

### Creating a new user

- Create the user
  - sudo useradd -m -d /home/u_mongo -s /bin/bash u_mongo
- Add a password to the user
  - sudo passwd u_mongo
- Create the ssh directory
  - sudo mkdir /home/u_mongo/.ssh
- Copy the ssh key in
  - sudo touch /home/u_mongo/.ssh/authorized_keys
    - Put the public keys into the file (however you want. Here are some options)
      - curl file_somewhere >> /home/u_mongo/.ssh/authorized_keys
      - Vim /home/u_mongo/.ssh/authorized_keys
- Set the directory permissions
  - sudo chown -R u_mongo:u_mongo /home/u_mongo/.ssh
  - sudo chmod 700 /home/u_mongo/.ssh
  - sudo chmod 600 /home/u_mongo/.ssh/authorized_keys
- Add a group
  - sudo usermod -a -G databases u_mongo

### Installing

- sudo apt-get install gnupg curl
- curl -fsSL <https://www.mongodb.org/static/pgp/server-7.0.asc> | sudo gpg -o usr/share/keyrings/mongodb-server-7.0.gpg --dearmor
- echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] <https://repo.mongodb.org/apt/ubuntu> jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
- sudo apt-get update
- sudo apt-get install -y mongodb-org

### Creating a link to the config file

- Create the directory
  - sudo mkdir /projects/configs/mongodb
- Edit the ownership and permission
  - sudo chmod u=rwx,g=rwx,o=rx /projects/configs/mongodb
  - sudo chown split_tracker:databases /projects/configs/mongodb
- Create the soft link
  - sudo ln -s /etc/mongod.conf /projects/configs/mongodb/mongod.conf

### Changing the dbPath (because I want to)

- Create the directory
  - sudo mkdir /projects/mnongodb
  - sudo chown mongodb:databases /projects/mongodb
  - sudo chmod u=rwx,g=rx,o= /projects/mongodb
- Go into the configuration file
  - sudo vim /etc/mongod.conf
- Edit the path in the storage section called dbPath
  - dbPath: /projects/mongodb

### Adding SSL

- MongoDB needs a special combined version of the ssl private key and full chain. So we have to cat those into a new file
    WILL NEED TO WRITE SOME SCRIPT TO AUTORENEW AND COMBINE THESE FILES FOR MONGO AT THE SAME TIME.
  - sudo cat /projects/ssl/live/youredomain.xxx/cert.pem /projects/ssl/live/youredomain.xxx/privkey.pem | sudo tee /projects/ssl/live/youredomain.xxx/mongo.pem > /dev/null
  - sudo chmod u=rwx,g=rwx,o=rx /projects/ssl/live/youredomain.xxx/mongo.pem

- Go into the configuration file
  - sudo vim /etc/mongod.conf
  - Add the following if using the ssl steps above to the new section. You will need to change the path to match the domain name you used. You can find it by running "sudo ls /projects/ssl/live/"
    - <pre><code>
    net: (don't put this part in add it to the existing section at the same level as port and bindIp)
       tls:
          mode: requireTLS
          certificateKeyFile: /projects/ssl/live/youredomain.xxx/mongo.pem
          CAFile: /projects/ssl/live/youredomain.xxx/fullchain.pem
          allowConnectionsWithoutCertificates: false
    </code></pre>
    - If for some reason you still want to allow connections without ssl you can change the follow line to
      - allowConnectionsWithoutCertificates: true

### Setting up

The configuration file can be found at "/etc/mongod.conf" if needed

- Add the created user to the group
  - sudo usermod -a -G databases mongodb

- Start the service
  - sudo systemctl start mongod
- Check the status
  - sudo systemctl status mongod
- Enable it on boot
  - sudo systemctl enable mongod
- To stop and restart it
  - sudo systemctl stop mongod
  - sudo systemctl restart mongod

- To use the shell
  - mongosh

## Installing Redis

### Creating a new user

- Create the user
  - sudo useradd -m -d /home/u_redis -s /bin/bash u_redis
- Add a password to the user
  - sudo passwd u_redis
- Create the ssh directory
  - sudo mkdir /home/u_redis/.ssh
- Copy the ssh key in
  - sudo touch /home/u_redis/.ssh/authorized_keys
    - Put the public keys into the file (however you want. Here are some options)
      - curl file_somewhere >> /home/u_redis/.ssh/authorized_keys
      - Vim /home/u_redis/.ssh/authorized_keyss
- Set the directory permissions
  - sudo chown -R u_redis:u_redis /home/u_redis/.ssh
  - sudo chmod 700 /home/u_redis/.ssh
  - sudo chmod 600 /home/u_redis/.ssh/authorized_keys
- Add a group
  - sudo usermod -a -G databases u_redis

### Installing

- sudo apt-get install lsb-release curl gpg
- curl -fsSL <https://packages.redis.io/gpg> | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
- sudo chmod 644 /usr/share/keyrings/redis-archive-keyring.gpg
- echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] <https://packages.redis.io/deb> $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
- sudo apt-get update
- sudo apt-get install redis

### Changing the data directory

- Create the directory
  - sudo mkdir /projects/redis
  - sudo chown redis:databases /projects/redis
  - sudo chmod u=rwx,g=rx,o= /projects/redis
- Go into the configuration file
  - sudo vim /etc/redis/redis.conf
- Edit the path in the storage section called dbPath
  - dbPath: /projects/redis

### Adding SSL

- Go into the configuration file
  - sudo vim /etc/redis/redis.conf
  - Find and modify, or add, the following. You will need to change the path to match the domain name you used. You can find it by running "sudo ls /projects/ssl/live/"
    - <pre><code>
    port 0
    tls-port 6379
    tls-cert-file /projects/ssl/live/youredomain.xxx/cert.pem
    tls-key-file /projects/ssl/live/youredomain.xxx/privkey.pem
    tls-ca-cert-file /projects/ssl/live/youredomain.xxx/chain.pem
    </code></pre>
- Test that it works
  - sudo systemctl start redis-server
  - sudo systemctl status redis-server
    - If it's active then good. If not check the paths you entered.
  - sudo systemctl stop redis-server

### Creating a link to the config file

- Create the directory
  - sudo mkdir /projects/configs/redis
- Edit the ownership and permission
  - sudo chmod u=rwx,g=rwx,o=rx /projects/configs/redis
  - sudo chown split_tracker:databases /projects/configs/redis
- Create the soft link
  - sudo ln -s /etc/redis/redis.conf /projects/configs/redis/redis.conf

### Setting up

The configuration file can be found at "/etc/redis/redis.conf" if needed

- Add the created user to the group
  - sudo usermod -a -G databases redis

- Start the service
  - sudo systemctl start redis-server
- Check the status
  - sudo systemctl status redis-server
- Enable it on boot
  - sudo systemctl enable redis-server

## Need to port forward

## Installing Python?

## Installing the code from github

## Setting up Backup with Rsync?

## Setting up Backup of Databases?

## Nginx set up? Reverse Proxies instead of ports?

- nginx is at "/etc/nginx"
- nginx available sites are at "/etc/nginx/sites-available"
- nginx enabled sites are at "/etc/nginx/sites-enabled"

## Setting up gunicorn for flask?

## Ports (Just Notes)

- SSH: 22
- PostgreSQL: 5432
- MongoDB: 27017
- Redis: 6379
- Flask:
- HTTP: 80
- HTTPS: 443
