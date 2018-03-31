#!/bin/sh
. venv/bin/activate
sudo docker-compose up -d

DB_CONN_STRING=postgres://app_user:password@localhost:5432/app_db python wait_for_postgres.py
DB_CONN_STRING=postgres://app_user:password@localhost:5432/app_db python -m unittest discover
sudo docker-compose down
