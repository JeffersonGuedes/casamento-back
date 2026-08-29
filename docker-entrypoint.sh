#!/bin/sh
set -e

mkdir -p /app/media /app/staticfiles
chown -R django:django /app/media /app/staticfiles

exec su django -s /bin/sh -c 'python manage.py migrate --noinput && python manage.py collectstatic --noinput && exec "$@"' sh "$@"