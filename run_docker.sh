#!/usr/bin/env bash

docker run --name zirkel -d -p 9000:5000 --restart always --env-file .env \
    --link postgres_db:dbserver \
    --mount source=zirkel-modules,target=/home/zirkel/.data \
    zirkel:latest
