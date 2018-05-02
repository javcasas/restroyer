import os
import psycopg2

pg = psycopg2.connect(os.environ["DB_CONN_STRING"])

def getPostgres(timeout=20):
    return pg.cursor()

def runMigration(fname):
    with open(fname) as f:
        migrations = f.read()
    getPostgres().execute("begin transaction; " + migrations + "commit;")

def runMigrations():
    resetDb()
    runMigration("../migrations/server_variables.sql")
    runMigration("../migrations/migrations.sql")
    runMigration("seed_db.sql")

def resetDb():
    with open("../migrations/undo_migrations.sql") as f:
        undo_migrations = f.read()
    getPostgres().execute("begin transaction; " + undo_migrations + "commit;")
