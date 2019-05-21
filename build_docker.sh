#!/usr/bin/env bash

cp ~/.ssh/id_rsa.korrespondenzzirkel .
docker build -t zirkel:latest .