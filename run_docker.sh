#!/usr/bin/env bash

docker run --name zirkel -d -p 9000:5000 --restart always --env-file .env \
    --link mysql:dbserver \
    zirkel:latest
