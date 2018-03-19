#!/bin/sh
sudo docker run --rm postgres psql postgres://app_user:password@192.168.1.8:5432/app_db -c "`cat migrations.sql`"
