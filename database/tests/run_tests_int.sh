#!/bin/sh
. venv/bin/activate

DB_CONN_STRING=postgres://app_user:password@localhost:5432/app_db python wait_for_postgres.py
DB_CONN_STRING=postgres://app_user:password@localhost:5432/app_db python -m unittest $@
