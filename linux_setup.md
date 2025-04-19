# Notes on Setting up Linux

Assuming using Ubuntu 22.04.1 LTS jammy

## Setting up basics

Maybe add notes on setting up the basic linux stuff like disabling passwords and enabling ssh keys and stuff later. Creating ssh key to connect to it from your client and stuff too.

- On your client machine, not the server
  - Make the ssh directory if you don't already have it
    - mkdir -p ~/.ssh && chmod 700 ~/.ssh
  - Create the config file if you don't already have it
    - touch ~/.ssh/config
    - chmod 600 ~/.ssh/config
  - Generate ssh keys
    - ssh-keygen -t ed25519 -f ~/.ssh/desired_name
  - Add it to your config file
    - <pre><code>
        Host desired_name
            HostName address_to_server
            User username
            Port 22
            IdentityFile ~/.ssh/desired_name
      </code></pre>
- Copy the key to your server
  - ssh-copy-id -i ~/.ssh/desired_name user@server
- Log into your server with a sudo user
  - ssh desired_name
- Allowing SSH
  - sudo apt install openssh-server
  - sudo systemctl enable ssh
  - sudo ufw allow ssh
- Disabling password based login
  - sudo vim /etc/ssh/sshd_config
    - Edit the following lines
        <pre><code>
        ChallengeResponseAuthentication no
        PasswordAuthentication no
        UsePAM no
        PermitRootLogin no
        #PermitRootLogin prohibit-password
        </code></pre>
  - Restart it
    - sudo systemctl reload ssh

## Setting up group

- Creating the group
  - sudo groupadd databases
- Add whatever user your currently using to the group
  - sudo usermod -a -G databases your_user
- Reload the user
  - sudo su - your_user

## Creating a user to access this project (for backups and stuff)

- Create the user
  - sudo useradd -m -d /home/u_split_tracker -s /bin/bash split_tracker
- Add a password to the user
  - sudo passwd split_tracker
- Create the ssh directory
  - sudo mkdir /home/u_split_tracker/.ssh
- Copy the ssh key in
  - sudo touch /home/u_split_tracker/.ssh/authorized_keys
    - Put the public keys into the file (however you want. Here are some options)
      - curl file_somewhere >> /home/u_split_tracker/.ssh/authorized_keys
      - Vim /home/u_split_tracker/.ssh/authorized_keys
- Set the directory permissions
  - sudo chown -R split_tracker:split_tracker /home/u_split_tracker/.ssh
  - sudo chmod 700 /home/u_split_tracker/.ssh
  - sudo chmod 600 /home/u_split_tracker/.ssh/authorized_keys
- Add a group
  - sudo usermod -a -G databases split_tracker

## Creating a directory to store files for this project

- Switch to the split_tracker user
  - sudo su split_tracker

- Create the directory
  - mkdir /projects
  - cd /projects
- Creating the directory for SSL
  - mkdir ssl
- Creating a directory for storing links to config files
  - mkdir configs
- Creating a directory for storing links to log files
  - mkdir logs

- Creating a directory to store the project files
  - mkdir split_tracker

- Changing the ownership and permissions
  - Change the ownership
    - chown -R split_tracker:databases /projects
  - Change the permissions
    - chmod -R u=rwx,g=rwx,o=rx /projects

- Exit the user
  - exit

- Changing the ownership of the base project folder (because you may have multiple projects)
  - sudo chown root:databases /projects

## Downloading the files for this project

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
      - You may also want to install this as well if using nginx
        - sudo /opt/certbot/bin/pip install certbot-nginx
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
      - Realistically you don't actually even need to do the mongo, postgres, and redis subdomains if they're all running locally on one machine or on a local network, you also wouldn't even need to set up ssl for them. However, while developing this I am using a separate server for the databases and my local machine for running the program. It's still on a local network though which negates the need for all of this ssl and domain actions, but it's a good learning experience to experiment with it. If you're running everything locally you can feel free to ignore everything involving ssl on the databases and their subdomains. However, you should still set up www and the base domain with ssl because you're going to need HTTPS if you're not a goober.
      - Also note that if using dynamic dns through ddclient you will need to add all the subdomains in there too.
    - Set up automatic renewal
      - <pre><code>echo "0 0,12 ** *root /opt/certbot/bin/python -c 'import random; import time; time.sleep(random.random()* 3600)' && sudo certbot renew -q" | sudo tee -a /etc/crontab > /dev/null</code></pre>
      - Since I want to use a different directory than default I did
        - <pre><code>echo "0 0,12 ** *root /opt/certbot/bin/python -c 'import random; import time; time.sleep(random.random()* 3600)' && sudo certbot renew --config-dir /projects/ssl -q" | sudo tee -a /etc/crontab > /dev/null<code></pre>
    - Manually renew certificates
      - sudo certbot renew -q
      - If using the custom location it's
        - sudo certbot renew --config-dir /projects/ssl -q
          - If it wont let you because of a port being in use do this
            - sudo netstat -tlnp | grep port#
            - sudo systemctl stop service_using_port
            - sudo certbot renew --config-dir /projects/ssl -q
              - Remove the -q flag if you want to see details
            - sudo systemctl start service_you_stopped
      - You can also check current certificates with this
        - sudo certbot certificates
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
      - That didn't seem to work so do this too
        - sudo chmod -R u=rwx,g=rx,o= /projects/ssl/
        - sudo chown -R root:databases /projects/ssl/
        - sudo chmod -R u=rwx,g=r,o= /projects/ssl/live/youre_domain/*
          - This is changing the permissions of a system link and it shouldn't change the permissions because the source file permissions are what matter, but it seemed to work.
    - Notes:
      - Certbot will return 4 files:
        - cert.pem
          - The public key. However, this one shouldn't be used with most software.
          - This is just the certificate.
        - chain.pem
          - The certificate chain.
          - This is the intermediary signed authority that is signed by the root authority.
        - fullchain.pem
          - The certificate that you will use in most server software. It is a combination of the cert.pem and the chain.pem
          - This is the crt file. Sometimes this is named as your_domain.crt
        - privkey.pem
          - The private key
          - This is the key file. Sometimes this is named as your_domain.key

## Alternative Self-Hosted SSL using OpenSSL

The rest of the documentation will be using path examples following the Let's Encrypt example. You will need to adjust the example paths if using this method.

- Install OpenSSL
  - sudo apt-get install openssl
- Creating the Certificate Authority Certificate and Keys
  - Create the self-signed certificate authority private key
    - I'm using RSA (it's the most common method)
      - sudo openssl genrsa -out /projects/ssl/self/yourdomain/ca.key 2048
    - I found server other ways to do this. Here are some examples.
      - Using Elliptic Curve instead
        - sudo openssl ecparam -name prime256v1 -genkey -noout -out /projects/ssl/self/yourdomain/ca.key
      - Using AES for an encrypted private key
        - sudo openssl genrsa -aes256 -out /projects/ssl/self/yourdomain/ca.key 4096
  - Create the self-signed certificate authority certificate
    - Creating a simple certificate
      - sudo openssl req -new -x509 -sha256 -nodes -days 365 -key /projects/ssl/self/yourdomain/ca.key -out /projects/ssl/self/yourdomain/ca.crt -subj "/CN=ca.yourdomain" --addext "subjectAltName=DNS:yourdomain,DNS:www.yourdomain,IP:YourIP"
        - Replace the CN with whatever your host, address, or domain is of the machine it's installed on.
          - Apparently this is actually wrong! You can name this whatever you want, but the CA, Server, and Client all need to have different values for it.
            - While that is true postgres actually needs it to match your hostname.
              - The important part of this is that the CN values don't really matter, except for on the certificate that the server is using! The certificate that the server is using is the one that needs to actually match the host that you'll be using to connect to the database. Not the CA but the actual certificate you'll be creating below.
                - I will be making separate client certificates in this example, but you can use the server ones on the client too.
        - The subjectAltName is the actual domains and IP addresses you are using. Adjust it to your needs and add as many as you want.
        - SSL Information
          - Distinguished Name (DN)
            - This contains a lot of information in the SSL certificate. This includes the Common Name, Organization, Organizational Unit, Locality, State, and Country.
          - Common Name (CN), or the Fully Qualified Domain Name (FQDN)
            - This is the value in the Distinguished Name (DN). It is made up of the host domain, such as "your_website.com", but isn't a url and doesn't contain any protocols, ports, etc.
          - Subject Alternative Name (SAN)
            - Used for letting a single certificate protect more than one website.
          - Organization (O)
            - What company or group owns this certificate.
          - Organizational Unit (OU)
            - What part of that organization owns this certificate.
          - Country (C)
            - The country where this certificate is from.
          - State (S)
            - What State or Province where this certificate is from.
          - Locality (L)
            - What city or town where this certificate is from.
          - Validity Period
            - When this certificate will expire and must be renewed, also the start date and time.
          - Issuing Certificate Authority (CA)
            - Who is issuing this certificate.
          - Serial Number
            - A unique identifier that is given to every SSL certificate.
          - Public Key
            - The public key of this SSL certificate. This lets users encrypt their information and send it to the server. The data will then be decrypted though the servers matching private key. The private key generates the public key. The private key can decrypt data encrypted with the public key, but the public key can't decrypt the data it encrypted. This lets anyone send the server securely encrypted information that only the server can decrypt. This is known as asymmetric encryption. It is a one-way encryption where one party with the public key can encrypt and one part with the private key can decrypt. As opposed to symmetric encryption where both parties would be able to encrypt and decrypt with the same key.
          - Signature Algorithm
            - This is an algorithm used to check if an SSL certificate is valid.
          - Key Usage (KU)
            - The activities that the key can perform and is supposed to do.
          - Extended Key Usage (EKU)
            - The activities that a key can perform, but doesn't specify if they should.
          - Certificate Policies
            - Policies that describe how the SSL certificate is to be used.
          - CRL Distribution Points (CDP)
            - A list of SSL certificates that aren't trustworthy.
          - Authority Information Access (AIA)
            - Where to find information about the issuer of the certificate.
          - Subject Key Identifier (SKI)
            - A unique identifier that is used to confirm that this is the right server to talk to.
          - Authority Key Identifier (AKI)
            - A unique identifier that is used to confirm that you're talking to the right authority.
          - Basic Constraints
            - Basic rules that tell connections what this certificate can do. Such as if it can create other certificates.
    - If you want to instead use prompts to answer all of the aspects of the Distinguished name.
      - sudo openssl req -new -x509 -sha256 -key /projects/ssl/self/yourdomain/ca.key -out /projects/ssl/self/yourdomain/ca.crt
    - You can also do these first 2 steps in one action using this commands
      - sudo openssl req -new -x509 -days 365 -nodes -text -out /projects/ssl/self/yourdomain/ca.crt -keyout /projects/ssl/self/yourdomain/ca.key -subj "/CN=ca.yourdomain" --addext "subjectAltName=DNS:yourdomain,DNS:www.yourdomain,IP:YourIP"
- Create the Server Certificate and Keys
  - Generating a private key for the server certificate
    - Using RSA again, if you want to use a different type refer to the first step
      - sudo openssl genrsa -out /projects/ssl/self/yourdomain/server.key 2048
  - Generate the server certificate signing request
    - sudo openssl req -new -sha256 -nodes -key /projects/ssl/self/yourdomain/server.key -out /projects/ssl/self/yourdomain/server.csr -subj "/CN=postgre.yourdomain" --addext "subjectAltName=DNS:yourdomain,DNS:www.yourdomain,IP:YourIP"
      - This is the very important part mentioned when generating the CA!
      - Instead of this you can create the private key and signing request in one step with
      - sudo openssl req -newkey rsa:2048 -days 365 -nodes -text -out /projects/ssl/self/yourdomain/server.crt -keyout /projects/ssl/self/yourdomain/server.key -subj "/CN=postgre.yourdomain" --addext "subjectAltName=DNS:yourdomain,DNS:www.yourdomain,IP:YourIP"
  - Generate the X509 certificate for the server, the certificate chain
    - sudo openssl x509 -req -sha256 -days 365 -CAcreateserial -in /projects/ssl/self/yourdomain/server.csr -CA /projects/ssl/self/yourdomain/ca.crt -CAkey /projects/ssl/self/yourdomain/ca.key -out /projects/ssl/self/yourdomain/server.crt
  - (Optional) If you need to combine the private key and public key together do this to create a pfx file.
    - sudo openssl pkcs12 -export -keypbe NONE -certpbe NONE -nomaciter -passout pass: -out /projects/ssl/self/yourdomain/server.pfx -inkey /projects/ssl/self/yourdomain/server.key -in /projects/ssl/self/yourdomain/server.crt
    - You can then convert it back into text like this I believe
      - sudo openssl rsa -in /projects/ssl/self/yourdomain/server.pfx -out /projects/ssl/self/yourdomain/server_nopass.pfx
    - To create an encrypted file use
      - sudo openssl pkcs12 -export -out /projects/ssl/self/yourdomain/server.pfx -inkey /projects/ssl/self/yourdomain/server.key -in /projects/ssl/self/yourdomain/server.crt
- Create the Client Certificate and Keys
  - Create the client certificate private key
    - Using RSA again, if you want to use a different type refer to the first step
      - sudo openssl genrsa -out /projects/ssl/self/yourdomain/client.key 2048
  - Generate the client certificate signing request
    - sudo openssl req -new -sha256 -nodes -key /projects/ssl/self/yourdomain/client.key -out /projects/ssl/self/yourdomain/client.csr -subj "/CN=client.yourdomain" --addext "subjectAltName=DNS:yourdomain,DNS:www.yourdomain,IP:YourIP"
      - Instead of this you can create the private key and signing request in one step with
      - sudo openssl req -newkey rsa:2048 -days 365 -nodes -text -out /projects/ssl/self/yourdomain/client.crt -keyout /projects/ssl/self/yourdomain/client.key -subj "/CN=client.yourdomain" --addext "subjectAltName=DNS:yourdomain,DNS:www.yourdomain,IP:YourIP"
  - Generate the X509 certificate for the client
    - sudo openssl x509 -req -sha256 -days 365 -CAcreateserial -in /projects/ssl/self/yourdomain/client.csr -CA /projects/ssl/self/yourdomain/ca.crt -CAkey /projects/ssl/self/yourdomain/ca.key -out /projects/ssl/self/yourdomain/client.crt
  - (Optional) If you need to combine the private key and public key together do this to create a pfx file.
    - sudo openssl pkcs12 -export -keypbe NONE -certpbe NONE -nomaciter -passout pass: -out /projects/ssl/self/yourdomain/client.pfx -inkey /projects/ssl/self/yourdomain/client.key -in /projects/ssl/self/yourdomain/client.crt
    - You can then convert it back into text like this I believe
      - sudo openssl rsa -in /projects/ssl/self/yourdomain/client.pfx -out /projects/ssl/self/yourdomain/client_nopass.pfx
    - To create an encrypted file use
      - sudo openssl pkcs12 -export -out /projects/ssl/self/yourdomain/client.pfx -inkey /projects/ssl/self/yourdomain/client.key -in /projects/ssl/self/yourdomain/client.crt
- Verifying the certificates
  - Verify the server certificate
    - sudo openssl verify -CAfile /projects/ssl/self/yourdomain/ca.crt /projects/ssl/self/yourdomain/ca.crt /projects/ssl/self/yourdomain/server.crt
      - You can also try this as well
        - sudo openssl verify -CAfile /projects/ssl/self/yourdomain/ca.crt -untrusted /projects/ssl/self/yourdomain/ca.crt /projects/ssl/self/yourdomain/server.crt
  - Verify the client certificate
    - sudo openssl verify -CAfile /projects/ssl/self/yourdomain/ca.crt /projects/ssl/self/yourdomain/ca.crt /projects/ssl/self/yourdomain/client.crt
      - You can also try this as well
        - sudo openssl verify -CAfile /projects/ssl/self/yourdomain/ca.crt -untrusted /projects/ssl/self/yourdomain/ca.crt /projects/ssl/self/yourdomain/client.crt
- Viewing information about the certificates
  - sudo openssl x509 -noout -text -in /projects/ssl/self/yourdomain/client.crt
    - If using a different encoding you may need to use one of these
      - sudo openssl x509 -inform pem -noout -text -in /projects/ssl/self/yourdomain/client.crt
      - sudo openssl x509 -inform der -noout -text -in /projects/ssl/self/yourdomain/client.crt
- Changing ownership and permissions
  - sudo chmod -R u=rwx,g=rx,o= /projects/ssl/self/yourdomain/
  - sudo chown -R root:databases /projects/ssl/self/yourdomain/
  - sudo chmod -R u=rwx,g=r,o= /projects/ssl/self/yourdomain/*
- Files
  - Certificate Authority
    - ca.crt
      - This is the public key for self-signed certificate authority certificate.
    - ca.key
      - This is the private key for the self-signed certificate authority.
  - Server
    - server.crt
      - This is the public key for the server.
    - server.key
      - This is the private key for the server.
    - server.csr
      - This is an intermediary file that contains the information needed to generate a SSL/TLS certificate.
  - Client
    - client.crt
      - This is the public key for the client.
    - client.key
      - This is the private key for the client.
    - client.csr
      - This is an intermediary file that contains the information needed to generate a SSL/TLS certificate.

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

### Creating a link to the log file

- Create the directory
  - sudo mkdir /projects/logs/postgres
- Edit the ownership and permission
  - sudo chmod u=rwx,g=rwx,o=rx /projects/logs/postgres
  - sudo chown split_tracker:databases /projects/logs/postgres
- Create the soft link
  - sudo ln -s /var/log/postgresql/postgresql-version#-main.log /projects/logs/postgres/postgresql-version#-main.log

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
    - Actually for postgres that one might be a lie because it starts other services. Do this instead.
      - sudo systemctl status 'postgresql*'
  - sudo systemctl stop postgresql

### Adding SSL

- Go into the configuration file
  - sudo vim /etc/postgresql/version#/main/postgresql.conf
  - Find and modify, or add, the following. You will need to change the path to match the domain name you used. You can find it by running "sudo ls /projects/ssl/live/"
    - <pre><code>
    ssl = on
    #ssl_ca_file = '/projects/ssl/live/youredomain.xxx/chain.pem'
    #ssl_cert_file = '/projects/ssl/live/youredomain.xxx/cert.pem'
    #ssl_ca_file = '/projects/ssl/live/youredomain.xxx/root_ca.pem'
    ssl_cert_file = '/projects/ssl/live/youredomain.xxx/fullchain.pem'
    ssl_key_file = '/projects/ssl/live/youredomain.xxx/privkey.pem'
    ssl_ciphers = 'HIGH:MEDIUM:+3DES:!aNULL'
    ssl_prefer_server_ciphers = on
    </code></pre>
  - Change the listening address!
    - By default postgres is listening to the localhost address, something like 127.0.0.1. Even when opening the port in ufw it wont really be open. It will only listen for connections from this machine, not your network! This stumped me for actual days because I thought either my router or isp was messed up, ufw was messed up, my iptables were messed up, or my ssl certificates were messed up. Nope! Just a setting I didn't know I needed to set!
      - Change the value in "listen_address" to the ip or host you want to listen to. I set mine to '0.0.0.0' to listen to every device. You can separate multiple addressed with commas. Note: The address does need to be a string, so put it in quotes.
        - IPv4: Local = 127.0.0.1 | All = 0.0.0.0
        - IPv6: Local = ::1 | All = ::
    - Note that if you want to change the port it listens to that line is right beneath this one. Note: This one is an integer.
- Add rule to allow for ssl
  - sudo vim /etc/postgresql/version#/main/pg_hba.conf
  - Add the following to the end
    - <pre><code>
    hostssl  all         all          0.0.0.0/0      md5
    </code></pre>
  - Note that this does not require ssl, it only allows the possibility of ssl. To require ssl you need to comment out all of the other "host" lines, at least the "all" ones (I'm not sure about the replication ones).
    - You can also comment out the "local" lines as well, but that's up to you. I probably wouldn't.
    - If you're intending to connect with the modes "disable", "allow", "prefer", or "require" that will work. However, if you're going to use "verify-ca" or "verify-full" you will need to do more work.
      - If you're using verify-ca you'll need to change the "md5" to "md5 clientcert=verify-ca"
      - If you're using verify-full you'll need to change the "md5" to "md5 clientcert=verify-full"
      - Note that these seem to be somewhat finicky (really not working) for me with Let's Encrypt. I believe it's because the CN in Let's Encrypt certificates are not your host name and PostgreSQL wants it to be. So it's probably best to either leave it as md5 or use the self-signed certificates.
  - (Optional) Testing domain with hosts.
    - sudo vim /etc/hosts
      - Add a line similar to
      - 127.0.0.1     your_domain
        - Comment this line out after testing. I don't think this actually works in a way that will test the certificate. Probably just skip this step.
  - If using the "verify-ca" or "verify-full" modes instead of required you will need to add a root certificate authority file.
    - Let's Encrypt
      - If you are using Let's Encrypt you need to download the certificate from Let's Encrypt. At the time of documenting this it can be obtained with the following command (however it may change in the future)
        - sudo curl -o /projects/ssl/live/youredomain.xxx/root_ca.pem "<https://letsencrypt.org/certs/isrgrootx1.pem>"
        - sudo chown --reference=/projects/ssl/live/youredomain.xxx/cert.pem /projects/ssl/live/youredomain.xxx/root_ca.pem && sudo chmod --reference=/projects/ssl/live/youredomain.xxx/cert.pem /projects/ssl/live/youredomain.xxx/root_ca.pem
      - Modify the config file
        - sudo vim /etc/postgresql/version#/main/postgresql.conf
        - <pre><code>
        ssl_ca_file = '/projects/ssl/live/youredomain.xxx/root_ca.pem'
        </code></pre>
    - Self-Signed Certificates
      - You should already have the ca file generated. Use that.

- Test that it works
  - sudo systemctl start postgresql
  - sudo systemctl status postgresql
    - If it's active then good. If not check the paths you entered.
  - sudo systemctl stop postgresql
    - sudo systemctl restart postgresql

### Setting up

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

### Setting up PostgreSQL

- Enter the shell as the super user
  - Change localhost to be your domain.
  - Chage the ssl parameters to the path to the copies of the certificates on your client.
  - Local Admin
    - sudo -u postgres psql
  - No SSL
    - sudo -u postgres psql "host=localhost port=5432"
      - sudo -u postgres psql "user=split_user host=localhost port=5432 dbname=split_tracker"
      - sudo -u postgres psql "user=split_user password=your_password host=localhost port=5432 dbname=split_tracker"
  - Required
    - sudo -u postgres psql postgres "sslmode=require host=localhost port=5432"
      - sudo -u postgres psql "user=split_user sslmode=require host=localhost dbname=split_tracker"
      - sudo -u postgres psql "user=split_user password=your_password sslmode=require host=localhost dbname=split_tracker"
  - Verify-CA
    - sudo -u postgres psql postgres "sslmode=verify-ca host=localhost port=5432 sslrootcert=root_ca.pem"
      - sudo -u postgres psql "user=split_user sslmode=verify-ca host=localhost port=5432 dbname=split_tracker sslrootcert=root_ca.pem"
      - sudo -u postgres psql "user=split_user password=your_password sslmode=verify-ca host=localhost port=5432 dbname=split_tracker sslrootcert=root_ca.pem"
  - Verify-Full
    - sudo -u postgres psql postgres "sslmode=verify-full host=localhost port=5432 sslrootcert=root_ca.pem sslcert=fullchain.pem sslkey=privkey.pem"
      - sudo -u postgres psql "user=split_user sslmode=verify-full host=localhost port=5432 dbname=split_tracker sslrootcert=root_ca.pem sslcert=fullchain.pem sslkey=privkey.pem"
      - sudo -u postgres psql "user=split_user password=your_password sslmode=verify-full host=localhost port=5432 dbname=split_tracker sslrootcert=root_ca.pem sslcert=fullchain.pem sslkey=privkey.pem"
- Create a password for your super user
  - \password postgres
- Create the user for the application
  - CREATE USER split_user WITH password 'your_password';
- Create the database for the application
  - CREATE DATABASE split_tracker;
- Grant the user permissions to the database
  - GRANT ALL PRIVILEGES ON DATABASE "split_tracker" to split_user;
- You can see user information with these commands
  - Commands
    - psql commands
      - \?
    - SQL commands
      - \help
  - Roles for users
    - \du
      - \du+
  - Databases
    - \l
  - List tables
    - \d

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

### Creating a link to the log file

- Create the directory
  - sudo mkdir /projects/logs/mongodb
- Edit the ownership and permission
  - sudo chmod u=rwx,g=rwx,o=rx /projects/logs/mongodb
  - sudo chown split_tracker:databases /projects/logs/mongodb
- Create the soft link
  - sudo ln -s /var/log/mongodb/mongod.log /projects/logs/mongodb/mongod.log

### Changing the dbPath (because I want to)

- Create the directory
  - sudo mkdir /projects/mongodb
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
          #CAFile: /projects/ssl/live/youredomain.xxx/root_ca.pem
          allowConnectionsWithoutCertificates: true
    </code></pre>
    - If you want the users to have to connect by providing a copy of the certificate change this. Otherwise they will need to connect with a copy of the certificate.
      - allowConnectionsWithoutCertificates: false
        - Note that like postgres I believe that this doesn't work well with Let's Encrypt. If you want to go this route I'd suggest using the self-signed certificate method.
  - Change the listening address
    - Change the "bindIp" in the net section as well to the domain or ip you're using. By default it will be local, something like 127.0.0.1. The same as PostgreSQL was. I will be changing mine to 0.0.0.0 to listen to all domains. You could also do 0.0.0.0,:: if you care about listening to IPv6 too and not just IPv4.
      - Note that the port is right above it if you want to change that.

### Optional: Setting kernel settings recommended for MongoDB

- MongoDB recommends that these settings are set.
- sudo vim /etc/sysctl.conf
  - Add this line in the file
    - <pre><code>
        vm.max_map_count = 131060
        fs.file-max = 98000
        kernel.pid_max = 64000
        kernel.threads-max = 64000
      </code></pre>
- sudo sysctl -p

### Setting up

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

### Setting up Mongodb

- If you are able to connect without opening the ports with SSL enabled good on you. I wasn't able to. Instead I did this temporarily.
  - sudo systemctl stop mongod
  - sudo vim /etc/mongod.conf
    - Change "mode: requireTLS" to "mode: preferTLS" or even "mode: allowTLS"
  - sudo systemctl start mongod
- To use the shell
  - Local Shell
    - sudo mongosh
  - No SSL
    - sudo mongosh --host yourdomain --port 27017
      - sudo mongosh --host yourdomain --port 27017 -u youruser -p yourpassword -authenticationDatabase yourdatabase
  - SSL No Certificates
    - sudo mongosh --host yourdomain --port 27017 --tls
      - sudo mongosh --host yourdomain --port 27017 --tls -u youruser -p yourpassword -authenticationDatabase yourdatabase
  - SSL With Certificates
    - sudo mongosh --host yourdomain --port 27017 --tls --tlsCAFile fullchain.pem
      - sudo mongosh --host yourdomain --port 27017 --tls --tlsCAFile fullchain.pem -u youruser -p yourpassword -authenticationDatabase yourdatabase
    - sudo mongosh --host yourdomain --port 27017 --tls --tlsCAFile fullchain.pem --tlsCertificateKeyFile mongo.pem
      - sudo mongosh --host yourdomain --port 27017 --tls --tlsCAFile fullchain.pem --tlsCertificateKeyFile mongo.pem -u youruser -p yourpassword -authenticationDatabase yourdatabase
- Helpful commands
  - Shows mongosh commands
    - help
  - Shows database comamnds
    - db.help()
  - You can run this to see your current user
    - db.runCommand({connectionStatus: 1})
      - Shouldn't really show anything now since we're the shell
  - Show the users
    - use admin
    - db.system.users.find()
  - Show the databases
    - show databases
  - Show all users
    - db.getSiblingDB('admin').system.users.find()
- Create a root user
  - use admin
  - db.createUser({user: "root", pwd: "your_password", roles : ["root"]})
- Create an admin user
  - db.createUser({user: "admin", pwd: "your_password", roles : [{role: "dbOwner", db: "admin"}]})
- Creating a database for the application
  - Create the database by switching to it
    - use split_tracker;
  - Create a table temporarily so that it will save the database
    - db.createCollection("users");
- Creating the user for the database
  - db.createUser({user: "split_user", pwd: "your_password", roles : [{role: "readWrite", db: "split_tracker"}]});
- Testing the user
  - db.auth("split_user", passwordPrompt())
    - db.auth("split_user", "your password)
- This is very important! By default you can log into mongoDB without any authnetication. We need to change that.
  - sudo vim /etc/mongod.conf
    - Edit, Add, or Modify the following:
    <pre><code>
    security:
      authorization: enabled
    </code></pre>
- If we changed this earlier change it back
  - exit
  - sudo vim /etc/mongod.conf
    - Change it back to "mode: requireTLS"
- Restart Mongo
  - sudo systemctl stop mongod
  - sudo systemctl start mongod
    - sudo systemctl restart mongod

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
- The following is a very important step! Without it redis will never properly shut down while using systemctl.
  - sudo vim /lib/systemd/system/redis-server.service
    - Add the following line to the "[Service]" section. Likely under the other similiar entries
      - <pre><code>
      ReadWriteDirectories=-/projects/redis
      </code></pre>
  - sudo systemctl daemon-reload

### Adding SSL

- Go into the configuration file
  - sudo vim /etc/redis/redis.conf
  - Find and modify, or add, the following. You will need to change the path to match the domain name you used. You can find it by running "sudo ls /projects/ssl/live/"
    - <pre><code>
    port 0
    tls-port 6379
    #tls-cert-file /projects/ssl/live/youredomain.xxx/cert.pem
    tls-cert-file /projects/ssl/live/youredomain.xxx/fullchain.pem
    tls-key-file /projects/ssl/live/youredomain.xxx/privkey.pem
    tls-ca-cert-file /projects/ssl/live/youredomain.xxx/chain.pem
    #tls-ca-cert-file /projects/ssl/live/youredomain.xxx/root_ca.pem
    tls-auth-clients yes
    </code></pre>
  - If you want the users to have to connect by providing a copy of the certificate change this. Otherwise they will need to connect with a copy of the certificate.
    - tls-auth-clients optional
      - You can also set this to "no" if you don't want to allow client certificates at all
      - Note that like postgres and mongodb I believe that this doesn't work well with Let's Encrypt. If you want to go this route I'd suggest using the self-signed certificate method.
  - Change the listening address!
    - Change the bind IP to the domain or ip you're using. By default it will be local, something like 127.0.0.1 -::1. The same as PostgreSQL and MongoDB were. I will be changing mine to 0.0.0.0 to listen to all domains. You could also do 0.0.0.0 :: if you care about listening to IPv6 too and not just IPv4.
      - The setting is just called "bind"
- Test that it works
  - sudo systemctl start redis-server
  - sudo systemctl status redis-server
  - sudo systemctl stop redis-server
    - Note that if redis has trouble stopping (did you modify the systemd file?) you can always manually kill the process using htop or the kill command after getting the pid with "ps -ax | grep -i redis"
  - sudo systemctl status redis-server
    - If it's active then good. If not check the paths you entered.
      - sudo systemctl restart redis-server

### Setting Up Users

- Redis has 3 options for users
  - Preferred: ACL
    - Go into the config file
      - sudo vim /etc/redis/redis.conf
    - ACL itself can be set up in 2 ways
      - Preferred: Using a seperate file
        - Add or modify the following
          - "aclfile /etc/redis/users.acl"
            - You can change the path if you want, but I'll leave mine as the default path.
          - Create the acl file if it's not already created
            - sudo touch /etc/redis/users.acl && sudo chown --reference=/etc/redis/ /etc/redis/users.acl && sudo chmod --reference=/etc/redis/ /etc/redis/users.acl
      - Not Preferred:
        - Add the ACL commands directly into the config file.
          - I wont be using this option but just add the lines would be similiar to this:
            - "user username on >your_password allcommands ~keys_to_match:*"
  - Not Preferred:
    - Just the default user with a password.
      - Go into the config file
        - sudo vim /etc/redis/redis.conf
      - Add or modify the following
        - "requirepass your_password"
      - This will set a password for the default user. This is from a time when redis didn't have ACL or users and only had one user. You should only use this if you don't care about having multiple users or user permissions.
  - Don't Do:
    - Don't use any users. Just an unprotected instance.

### Optional: Enable vm.overcommit_memory

- Redis may alert you that you need to add vm.overcommit_memory.
- sudo vim /etc/sysctl.conf
  - Add this line in the file
    - <pre><code>
        vm.overcommit_memory = 1
      </code></pre>
- sudo sysctl -p

### Creating a link to the config file

- Create the directory
  - sudo mkdir /projects/configs/redis
- Edit the ownership and permission
  - sudo chmod u=rwx,g=rwx,o=rx /projects/configs/redis
  - sudo chown split_tracker:databases /projects/configs/redis
- Create the soft link
  - Main config file
    - sudo ln -s /etc/redis/redis.conf /projects/configs/redis/redis.conf
  - If you're using the acl file add it too
    - sudo ln -s /etc/redis/users.acl /projects/configs/redis/users.acl
      - Note that you can make a symbolic link even if the redis file doesn't exist yet.
        - You wouldn't be able to make a hard link with "sudo ln /etc/redis/users.acl /projects/configs/redis/users.acl"

### Creating a link to the log file

- Create the directory
  - sudo mkdir /projects/logs/redis
- Edit the ownership and permission
  - sudo chmod u=rwx,g=rwx,o=rx /projects/logs/redis
  - sudo chown split_tracker:databases /projects/logs/redis
- Create the soft link
  - sudo ln -s /var/log/redis/redis-server.log /projects/logs/redis/redis-server.log

### Setting up

- Add the created user to the group
  - sudo usermod -a -G databases redis
- Start the service
  - sudo systemctl start redis-server
- Check the status
  - sudo systemctl status redis-server
- Enable it on boot
  - sudo systemctl enable redis-server

# Setting up Redis users with ACL

- Enter the local shell
  - sudo redis-cli
    - You may need to try one of these if they aren't working
      - sudo redis-cli -h 127.0.0.1
      - sudo redis-cli --tls
      - sudo redis-cli -h 127.0.0.1 --tls
- Create an admin user
  - acl setuser admin on >your_password allcommands allkeys
- You can do these for more information
  - Redis help
    - help
  - Help list for acl
    - acl help
  - List of users
    - acl list
  - Show users
    - acl users
  - Get a specific user
    - acl getuser user_name
  - Help
    - help
    - help command_name
  - Commands
    - command List
  - Show keys
    - Keys *
  - Set key
    - set key value
    - json.set key $ '{"normal": "json"}'
  - Get key
    - get key
    - json.get key $..path
  - Delete Key
    - del key
    - json.del key $..path
  - Flush Keys
    - Flushall
  - Expiring Keys
    - Expire key seconds NX
  - select #
    - Selects a specific database instance on redis. by default there are 16 and this can be edited in the config file by changing the "databases" setting.
  - Index
    - ft.create index on hash  prefix 1 key:field: schema field-x text sortable
  - Search
    - ft.search index search
    - ft.search index "@field: search"
  - Aggregate
    - ft.aggregate index * Groupby 1 @fieldReduce count 0 as output_name
- Create a user for the application to use
  - Create the user
    - acl setuser split_tracker on >your_password
  - Allow the user to be able to use all commands, but only on keys the start with "split_tracker:"
    - acl setuser split_tracker allcommands ~split_tracker:*
      - You can clear the commands by doing "nocommands"
      - You can remove commands by doing "-commandName"
      - You can add commands by doing "-commandsName"
      - You can remove all key patterns with "resetkeys"
      - You can add key patterns with "~keyPattern", with read and write permissions
      - You can do "%R~keyPattern" to add a key pattern with only read permissions
      - You can do "%W~keyPattern" to add a key pattern with only write permissions
      - You can set if a user is able to be logged into by setting the user to "on" or "off".
- Create a user for celery to use
  - Create the user
    - acl setuser celery on >your_password
  - Allow the user to be able to use all commands, but only on keys the start with "_kombu"
    - acl setuser celery allcommands ~_kombu*
      - I'm not sure about this one yet. ############################# I believe celery always adds that to the keys it adds, but maybe I'm wrong.
- Disable the default user
  - acl setuser default off
    - This should prevent any anonymous connections now
  - acl setuser default >your_password
    - We need to add a password to the default user or else redis will start in protected mode
- Saving the users
  - Redis doesn't seem to persist these by default. Instead you have to follow one of these options.
  - Preferred: Save the ACL in a seperate file (use this if you set up an ACL file in the config)
    - ACL SAVE
      - You can also use "ACL LOAD" to reload an acl file if you made changes to it externally.
  - Not Preferred: Rewrite the config file (only use this if you forgot to set up the config to use an ACL file)
    - CONFIG REWRITE

- You could also change the setting "protected-mode" from "yes" to "no", but that seems much less secure.

### Setting up Redis

- Enter redis
  - Local Shell
    - sudo redis-cli -n database#
  - No SSL
    - sudo redis-cli -n database# -h yourdomain -p 6379
      - sudo redis-cli -n database# -h yourdomain -p 6379 --user ACL_User --pass ACL_PASS
        - sudo redis-cli -n database# -h yourdomain -p 6379 --user ACL_User --askpass
  - SSL No Certificates
    - sudo redis-cli -n database# -h yourdomain -p 6379 --tls
      - sudo redis-cli -n database# -h yourdomain -p 6379 --user ACL_User --pass ACL_PASS --tls
        - sudo redis-cli -n database# -h yourdomain -p 6379 --user ACL_User --askpass --tls
  - SSL With Certificates
    - sudo redis-cli -n database# -h yourdomain -p 6379 --tls --cert cert.pem --key privkey.pem --cacert chain.pem
      - sudo redis-cli -n database# -h yourdomain -p 6379 --user ACL_User --pass ACL_PASS --tls --cert cert.pem --key privkey.pem --cacert chain.pem
        - sudo redis-cli -n database# -h yourdomain -p 6379 --user ACL_User --askpass --tls --cert cert.pem --key privkey.pem --cacert chain.pem
- Login to redis-cli (if you didn't pass the information)
  - With auth command
    - redis-cli
      - auth username password
- Shutting down redis
  - shutdown
    - Do this while inside of redis-cli to shut the server off

## Port Forwarding

### Needed for databases

- Port Forwarding on the Server
  - PostgreSQL
    - The default port is 5432
    - sudo ufw allow 5432 comment 'Split_Tracker: PostgreSQL'
      - sudo ufw allow from any to any port 5432 proto tcp comment 'Split_Tracker: PostgreSQL'
        - If we only want to allow the connection from a known address use this
          - sudo ufw allow from ip_address_from to any port 5432 proto tcp comment 'Split_Tracker: PostgreSQL'
  - MongoDB
    - The default port is 27017
    - sudo ufw allow 27017 comment 'Split_Tracker: MongoDB'
      - sudo ufw allow from any to any port 27017 proto tcp comment 'Split_Tracker: MongoDB'
        - To allow only from a specific IP adjust like the PostgreSQL example
  - Redis
    - The default port is 6379
    - sudo ufw allow 6379 comment 'Split_Tracker: Redis'
      - sudo ufw allow from any to any port 6379 proto tcp comment 'Split_Tracker: Redis'
        - To allow only from a specific IP adjust like the PostgreSQL example

### Probably need

- Flask
  - The default port is 5000
  - sudo ufw allow from any to any port 5000 proto tcp comment 'Split_Tracker: Flask'
    - To allow only from a specific IP adjust like the PostgreSQL example

- Reload ufw
  - sudo ufw reload

- Port Forwarding on your router or VPS
  - This will depend on your specific device or server provider. You will have to follow their instructions.
  - You will need to do this if you're using SSL. You could possibly use a self signed certificate instead of Let's Encrypt. However, if you followed these instructions and are using a domain you will need to forward the port publically.

- Testing the ports are open with telnet
  - telnet your_domain_or_ip port
- Checking ports with netstat
  - netstat -an | grep LISTEN
  - netstat -an | grep -i listen
  - netstat -l
  - sudo netstat -tunpl
- Checking iptables
  - sudo iptables -L -v -n
  - sudo iptables -t nat -L -v -n
- Checking ufw
  - sudo ufw status
- Checking ports with lsof
  - sudo lsof -nP -iTCP -sTCP:LISTEN
- Checking with ss
  - ss -tuln

### Possible

- HTTP
  - The default port is 80
  - sudo ufw allow from any to any port 80 proto tcp comment 'Split_Tracker: HTTP'
    - To allow only from a specific IP adjust like the PostgreSQL example
- HTTPS
  - The default port is 443
  - sudo ufw allow from any to any port 443 proto tcp comment 'Split_Tracker: HTTPS'
    - To allow only from a specific IP adjust like the PostgreSQL example
- SSH
  - The default port is 22
  - sudo ufw allow from any to any port 22 proto tcp comment 'Split_Tracker: SSH'
    - To allow only from a specific IP adjust like the PostgreSQL example

## Installing Python?

## Installing the code from github

## Setting up Backup with Rsync?

## Setting up Backup of Databases?

## Nginx set up? Reverse Proxies instead of ports?

- nginx is at "/etc/nginx"
- nginx available sites are at "/etc/nginx/sites-available"
- nginx enabled sites are at "/etc/nginx/sites-enabled"

## Setting up gunicorn for flask?
