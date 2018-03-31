import unittest
import os
import time
import requests
import psycopg2
from psycopg2.extensions import parse_dsn

pg = psycopg2.connect(os.environ["DB_CONN_STRING"])

def getPostgres(timeout=20):
    return pg.cursor()

def runMigrations():
    with open("../migrations/migrations.sql") as f:
        migrations = f.read()
    getPostgres().execute("begin transaction; " + migrations + "commit;")

def resetDb():
    with open("../migrations/undo_migrations.sql") as f:
        undo_migrations = f.read()
    getPostgres().execute("begin transaction; " + undo_migrations + "commit;")
