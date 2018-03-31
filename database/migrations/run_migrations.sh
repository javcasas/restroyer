#!/bin/sh
sudo docker exec -it restroyer_db_1 psql postgres://app_user:password@localhost:5432/app_db -c "`cat migrations.sql`"
