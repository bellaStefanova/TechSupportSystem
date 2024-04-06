set -o errexit
sed -i -e 's/\r$//' '/opt/startup/startup.sh'
source antenv/bin/activate
python manage.py qcluster &

gunicorn --bind=0.0.0.0 --timeout 600 TechSupportSystem.wsgi --access-logfile '-' --error-logfile '-'

