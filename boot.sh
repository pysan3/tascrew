#!/bin/bash
export RUN_PLACE='localhost'
export DATABASE_URL='sqlite:///app/database.sqlite3'

python create_events.py $@
