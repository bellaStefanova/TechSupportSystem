import os

from django.core.wsgi import get_wsgi_application

print(os.environ)
if os.environ.get('DBHOST') != None:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TechSupportSystem.deployment')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TechSupportSystem.settings')

# settings_module = "TechSupportSystem.deployment" if 'DBHOST' in os.environ else 'TechSupportSystem.settings'

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()
