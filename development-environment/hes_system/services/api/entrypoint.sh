#!/bin/sh

if [ "$DATABASE" = "postgresql" ]
then
  echo "Waiting for PostgreSQL..."
  while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
  done
  echo "PostgreSQL started."
fi


if [ "$FLASK_ENV" = "development" ]
then
  python manage.py create_db
  python manage.py fill_db
fi

exec "$@"
