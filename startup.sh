#!/usr/bin/env bash

echo "Start sshd"
/usr/sbin/sshd
python manage.py qcluster &

gunicorn --bind=0.0.0.0 --timeout 600 TechSupportSystem.wsgi --access-logfile '-' --error-logfile '-'

