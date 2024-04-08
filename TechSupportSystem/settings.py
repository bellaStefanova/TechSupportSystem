from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


AUTH_USER_MODEL = "accounts.UserProfile"

# SECRET_KEY = 'django-insecure-fxj8dsj^^q#pe7riz%&(7^bsr1a66#!48*dg)6#2k3%h)!525n'

# DEBUG = True

# ALLOWED_HOSTS = ['*']

SECRET_KEY = os.environ.get('SECRET', 'django-insecure-fxj8dsj^^q#pe7riz%&(7^bsr1a66#!48*dg)6#2k3%h)!525n')
DEBUG = os.environ.get('DEBUG', True)

ALLOWED_HOSTS = [os.environ.get('DJANGO_HOST', '127.0.0.1')]
CSRF_TRUSTED_ORIGINS = ['https://' + os.environ.get('WEBSITE_HOSTNAME', 'localhost')]
SECURE_SSL_REDIRECT=0
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'TechSupportSystem.web.apps.WebConfig',
    'TechSupportSystem.accounts.apps.AccountsConfig',
    'TechSupportSystem.departments.apps.DepartmentsConfig',
    'TechSupportSystem.requests.apps.RequestsConfig',
    'TechSupportSystem.notifications.apps.NotificationsConfig',
]

ROOT_URLCONF = 'TechSupportSystem.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

TEMPLATE_DIRS = (BASE_DIR / 'templates',)

WSGI_APPLICATION = 'TechSupportSystem.wsgi.application'


if 'DBHOST' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ['DBNAME'],
            'USER': os.environ['DBUSER'],
            'PASSWORD': os.environ['DBPASS'],
            'HOST': os.environ['DBHOST'] + '.postgres.database.azure.com',
            'PORT': '5432',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'techsupportsystem_db',
            'USER': 'root',
            'PASSWORD': 'Test',
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }

LOGIN_URL = 'signin'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
