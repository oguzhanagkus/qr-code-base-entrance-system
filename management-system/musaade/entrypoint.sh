#!/bin/sh

DONE_FILE=".done"

if [ "$DATABASE" = "postgresql" ]
then
  echo "Waiting for PostgreSQL..."
  while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
  done
  echo "PostgreSQL started."
fi

# Only run migrations if the .done file does not exist
if [ ! -f "$DONE_FILE" ]
then
  python manage.py migrate
  python manage.py createsuperuser --no-input --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL
  python manage.py makemigrations
  python manage.py migrate
  python manage.py collectstatic --no-input --clear
  mkdir -p data/keys
  touch $DONE_FILE
fi

exec "$@"
