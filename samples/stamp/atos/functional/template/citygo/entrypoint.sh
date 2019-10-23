#!/bin/sh

#Starting gunicorm
echo Starting Gunicorm

#python manage.py migrate --no-input
python manage.py collectstatic --no-input

# Run coverage 

#coverage run manage.py test -v 2
#coverage html
export BROWSER=firefox
exec "$@"

