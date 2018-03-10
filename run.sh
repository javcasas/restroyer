#!/bin/sh
sudo docker run --rm --name tutorial -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres

sudo docker exec -it tutorial bash -c "
while ! psql -U postgres -c '' 2> /dev/null; do   
  sleep 0.1 # wait for 1/10 of the second before check again
done
"
sudo docker exec -it tutorial bash -c "
while ! psql -U postgres -c '' 2> /dev/null; do   
  sleep 0.1 # wait for 1/10 of the second before check again
done
"
sudo docker exec -it tutorial bash -c "
while ! psql -U postgres -c '' 2> /dev/null; do   
  sleep 0.1 # wait for 1/10 of the second before check again
done
"
sh ./run_migrations.sh
sudo docker exec -it tutorial pg_dump -s -U postgres > .restroyer/schema.sql
sudo docker stop tutorial
