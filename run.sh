#!/bin/bash

# Start PostgreSQL
service postgresql start

# Initialize the database
psql -U $POSTGRES_USER -d $POSTGRES_DB -f /docker-entrypoint-initdb.d/init.sql

# Start Apache
service apache2 start

# Start pgAdmin4
service apache2 restart

# Keep the container running
tail -f /dev/null
