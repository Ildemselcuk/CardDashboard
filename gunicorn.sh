#!/bin/sh
cd app
flask db init
flask db migrate
flask db upgrade
cd ..
gunicorn main:app --bind 0.0.0.0:8000 --workers 3  --timeout 120 --log-level=debug