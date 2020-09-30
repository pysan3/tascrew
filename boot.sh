#!/bin/bash
export RUN_PLACE='localhost'
export DATABASE_URL='sqlite:///app/database.sqlite3'
export HASHID_SALT='tascrewLOCAL'

python create_events.py $@
