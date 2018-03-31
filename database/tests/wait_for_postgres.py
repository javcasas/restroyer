import unittest
import os
import time
import requests
import psycopg2
from psycopg2.extensions import parse_dsn

def waitForPostgres(timeout=20):
    for i in range(timeout * 10):
        try:
            conn = psycopg2.connect(os.environ["DB_CONN_STRING"])
            cur = conn.cursor()
            cur.execute("select * from pg_tables")
            return conn
        except psycopg2.OperationalError:
            time.sleep(0.1)

waitForPostgres()
waitForPostgres()
