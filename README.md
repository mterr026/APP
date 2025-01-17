﻿# EMPLOYEE BIDDING SYSTEM
This app is used for the USPS maintenance department to transition from the current paper based system to a web based application. the sytem manages authentication, bid postings, bid viewing, selection and awarding. 

# INSTALLATION
Prerequisites: 
    -python 3.x
    -PostgreSQL
    -Apache
    -pgAdmin4(for admin purposes)

    STEP 1
    -In the terminal of the server run the following command:

      pip install -r requirements.txt

    STEP 2
    -install postgreSQL for Ubuntu servers the commands are below:

        sudo apt update

        sudo apt install postgresql postgresql-contrib

        sudo systemctl start postgresql.service

    STEP 3
    -install pgadmin4:

        curl -fsS https://www.pgadmin.org/static/packages_pgadmin_org.pub | sudo gpg --dearmor -o /usr/share/keyrings/packages-pgadmin-org.gpg

        sudo sh -c 'echo "deb [signed-by=/usr/share/keyrings/packages-pgadmin-org.gpg] https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/$(lsb_release -cs) pgadmin4 main" > /etc/apt/sources.list.d/pgadmin4.list && apt update'

        sudo apt install pgadmin4-web 

        sudo /usr/pgadmin4/bin/setup-web.sh

# SETUP APACHE2 FOR REVERSE PROXY

    STEP 1
    -install the required Apache modules

        sudo a2enmod proxy proxy_http
        sudo systemctl restart apache2

    STEP 2
    - find and edit the configuration file 000-default.conf

        EXAMPLE: /etc/apache2/sites-available/000-default.conf

    STEP 3
    - replace the contents with the text below:
        #<VirtualHost *:80>
        #   ServerName yourdomain.com

        #    ProxyPass / http://127.0.0.1:8000/
        #    ProxyPassReverse / http://127.0.0.1:8000/

        #    ErrorLog ${APACHE_LOG_DIR}/error.log
        #    CustomLog ${APACHE_LOG_DIR}/access.log combined
        #</VirtualHost>

    STEP 4
    -restart apache:

        sudo systemctl restart apache2

# RUNNING THE APPLICATION

-To start the server to run the commnad:

    uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# FILE DESCRIPTIONS

    Python Files:
- requirements.txt: Lists all Python package dependencies for the project.

- classes.py: class definitions for the application's logic

- dependencies.py: Defines dependencies needed for the application, such as database connections

- main.py: The entry point of the FastAPI application, setting up the app and routes.

- businessLogic.py: the core business logic of the application, handling data processing, validation

- routers.py: defines the routes and directs to each endpoint

- schemas.py: Pydantic models for request and response data validation and serialization.

- CRUD.py: functions for Create, Read, Update, and Delete operations, typically interacting with the database.

- database.py: Sets up the database connection

- models.py: SQLAlchemy models that map to database tables, representing the application's data structure.

HTML Files:
- base.html: The base template that other templates use for common structure

- login.html: login page template

- firstLogin.html: for initial login, 
- employeeView.html: A template for displaying employee-specific views, such as dashboards or data.

- userManagement.html: The template for managing users, including listing, adding, and removing users.

- updateUser.html: for updating user credentials

- createUser.html: template for creating new users

- bidManagement.html: template for managing all bids, 

- createBid.html: template for creating bids

- editBid.html: template for editing bids

- bidDetails.html: template for displaying bids

