#!/usr/bin/env bash

source venv/bin/activate
flask db upgrade

exec gunicorn -b :5000 --access-logfile /dev/null --error-logfile - website:app
