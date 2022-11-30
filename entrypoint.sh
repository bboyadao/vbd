#!/bin/bash
python manage.py migrate
python manage.py collectstatic --noinput
echo "startting appication"
daphne -b 0.0.0.0 -p 8000 vin_bigdata.asgi:application