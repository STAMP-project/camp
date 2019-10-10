#!/bin/sh

python manage.py migrate --no-input
python manage.py collectstatic --no-input

gunicorn citygo_settings.wsgi:application -b 0.0.0.0:8003 --workers 3

#coverage run manage.py test -v 2
#coverage html
export BROWSER=firefox
exec "$@"

