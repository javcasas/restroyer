import unittest
import os
import time
import requests
import psycopg2
from psycopg2.extensions import parse_dsn
import requests

def waitForPostgres(timeout=20):
    for i in range(timeout * 10):
        try:
            conn = psycopg2.connect(os.environ["DB_CONN_STRING"])
            cur = conn.cursor()
            cur.execute("select * from pg_tables")
            return conn
        except psycopg2.OperationalError:
            time.sleep(0.1)

def waitForPostgREST(timeout=20):
    for i in range(timeout * 10):
        req = requests.get("http://localhost:3000/", timeout=0.1)
        if req.status_code == 400:
            # If there is no 'web_anon' role, it returns an error 400
            # but by then PostgREST is able to query PostgreSQL
            return
        time.sleep(0.1)
    else:
        raise Exception("PostgREST not available")

waitForPostgres()
waitForPostgres()
waitForPostgres()
waitForPostgREST()
