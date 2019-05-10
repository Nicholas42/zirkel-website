#!/usr/bin/env bash

# Load Variables from .env. Needs:
# POSTGRES_USER (=zirkel)
# POSTGRES_DB (=zirkel)
# POSTGRES_PASSWORD

docker run --name postgres_db -d --env-file .env postgres