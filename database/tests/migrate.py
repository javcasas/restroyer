import os
import psycopg2

pg = psycopg2.connect(os.environ["DB_CONN_STRING"])

def getPostgres(timeout=20):
    return pg.cursor()

def runMigrations():
    with open("../migrations/migrations.sql") as f:
        migrations = f.read()
    getPostgres().execute("begin transaction; " + migrations + "commit;")
    with open("seed_db.sql") as f:
        seed = f.read()
    getPostgres().execute("begin transaction; " + seed + "commit;")

def resetDb():
    with open("../migrations/undo_migrations.sql") as f:
        undo_migrations = f.read()
    getPostgres().execute("begin transaction; " + undo_migrations + "commit;")
