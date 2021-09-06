# Gyro SG Server
This contains the code for the Gyro SG API server and migrations for the postgres database.  

## Setup on Dev environment
Setup your python virtual environment:
```
bin/build_env.sh
```

Setup your environment variables:  
Create a .env file in the base directory gyrosg.  
Example .env file:
```.env
DB_HOST=localhost
DB_USER=gyrosg
DB_PASSWORD=gyrosg
DB_PORT=5432
DB_NAME=gyrosg
FIRST_SUPERUSER=gyrosg_admin@gyrosg.com
FIRST_SUPERUSER_PASSWORD=gyrosg_admin
```

Create the secrets.txt in the base directory gyrosg which is used to generate the tokens. 
```
touch secrets.txt
bin/generate_token.py > secrets.txt
```

Install your own postgres database locally (ubuntu):
```
sudo apt update
sudo apt install postgresql postgresql-contrib
```

Create the gyrosg user in the local postgres database:
```
sudo -u postgres psql
postgres=# CREATE ROLE gyrosg CREATEDB LOGIN PASSWORD 'gyrosg'; 
```

Create the dev database:
```
make create-dev-db
```

Run the SQL migrations:
```
make migrate-dev
```

Initializing data:
```
make init-data
```

### Cleaning and rebuilding your database schemas
Run 
```
make clean-dev-db
make migrate-dev
```

## Starting the Server
Run 
```
make run-dev
```

## To login to the ec2 instance
ssh -i "~/.ssh/gyrosg-server.pem" ec2-user@ec2-54-254-7-97.ap-southeast-1.compute.amazonaws.com

## Setting up on ec2 instance
Install your own postgres database locally (ubuntu):
```
sudo apt update
sudo apt install postgresql postgresql-contrib
```

Create the gyrosg user in the local postgres database:
```
sudo -u postgres psql
postgres=# CREATE ROLE gyrosg CREATEDB LOGIN PASSWORD 'gyrosg'; 
```

Setup your python virtual environment:
```
bin/build_env.sh
```

Setup your environment variables:  
Create a .env file in the base directory gyrosg.  
Example .env file:
```.env
DB_HOST=localhost
DB_USER=gyrosg
DB_PASSWORD=gyrosg
DB_PORT=5432
DB_NAME=gyrosg
FIRST_SUPERUSER=gyrosg_admin@gyrosg.com
FIRST_SUPERUSER_PASSWORD=gyrosg_admin
```


Create the secrets.txt in the base directory gyrosg which is used to generate the tokens. 
```
touch secrets.txt
bin/generate_token.py > secrets.txt
```

Create the gyrosg user in the local postgres database:
```
sudo -u postgres psql
postgres=# CREATE ROLE gyrosg CREATEDB LOGIN PASSWORD 'gyrosg'; 
```

Create the dev database:
```
make create-prod-db
```

Initializing data and migrations:
```
make init-db
```

Running the server:
```
bin/run.sh
```

## API Docs
To view the API docs, please access http://localhost:30009/docs after starting the server.
