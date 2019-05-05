#!/bin/bash

export FLASK_APP=main.py
flask db init
flask db migrate
flask db upgrade
echo '[+] Environment variable created'
echo '[+] Starting server'
FLASK_DEBUG=1 FLASK_ENV=development flask run --host=0.0.0.0
