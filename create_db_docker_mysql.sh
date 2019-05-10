#!/usr/bin/env bash

# Load Variables from .env. Needs:
# MYSQL_RANDOM_ROOT_PASSWORD (=yes)
# MYSQL_DATABASE (=zirkel)
# MYSQL_USER (=zirkel)
# MYSQL_PASSWORD
docker run --name mysql -d --env-file .env\
    mysql/mysql-server:5.7
