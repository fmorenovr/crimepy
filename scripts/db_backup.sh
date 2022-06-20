#!/usr/bin/bash

su -l postgres

db_name = $1

psql -d $db_name -a -f /home/fmorenovr/Downloads/data/crimebb-${db_name}.sql
