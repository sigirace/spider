#!/bin/sh

# Django 마이그레이션 수행
poetry run python manage.py makemigrations
poetry run python manage.py migrate

# Gunicorn을 사용하여 Django 앱 실행
poetry run gunicorn --workers 3 --bind unix:/tmp/gunicorn.sock config.wsgi:application &

# Celery 워커 실행 (백그라운드에서 실행)
poetry run celery -A config worker --loglevel=debug&

echo "Starting Nginx..."
nginx -g "daemon off;"