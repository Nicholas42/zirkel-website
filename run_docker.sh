#!/usr/bin/env bash

docker run --name zirkel -d -p 8000:5000 --restart always --env-file .env \
    --link mysql:dbserver \
    zirkel:latest
