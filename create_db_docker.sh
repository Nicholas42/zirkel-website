#!/usr/bin/env bash

docker run --name mysql -d -e MYSQL_RANDOM_ROOT_PASSWORD=yes \
    -e MYSQL_DATABASE=zirkel -e MYSQL_USER=zirkel \
    -e MYSQL_PASSWORD=${DB_PASS} \
    mysql/mysql-server:5.7
