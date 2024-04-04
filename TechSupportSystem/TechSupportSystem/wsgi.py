import os

from django.core.wsgi import get_wsgi_application

settings_module = 'TechSupportSystem.deployment' if 'SCM_DO_BUILD_DURING_DEPLOYMENT' in os.environ else 'TechSupportSystem.settings'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()
