"""
Django settings for tvdordrecht project.

"""

from os import path
import json

# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception. :P
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = path.abspath(path.join(path.dirname(__file__), "..", ".."))
PROJECT_DIR = path.abspath(path.join(path.dirname(__file__), ".."))
SECRETS_FILE = path.normpath(path.join(BASE_DIR, 'secrets.json'))

with open(SECRETS_FILE) as f:
    secrets = json.loads(f.read())

def get_secret(setting, default=None):
    """Get the secret variable or default or return explicit exception."""
    if default is not None:
        return secrets.get(setting, default)
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {0} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret("SECRET_KEY")

# TODO: This should be a tuple in secrets.json.
SITE_ADMIN = get_secret("SITE_ADMIN")
ADMINS = (('Coen', SITE_ADMIN), )

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [
    'tvdordrecht.nl',
    'www.tvdordrecht.nl',
    '149.210.227.54',
    'tvdwedstrijd.nl',
    'www.tvdwedstrijd.nl',
]

SITE_ID = 1

# Application definition
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'formtools',
    'crispy_forms',
    'tvdordrecht',
    'webapp',
    'swimtest',
    'training',
    'race',
    'django.contrib.admin',
]

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'webapp.middleware.ThreadLocals',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.messages.context_processors.messages',
    'django.contrib.auth.context_processors.auth',
    'webapp.context_processors.basics'
)

ROOT_URLCONF = 'tvdordrecht.urls'

WSGI_APPLICATION = 'tvdordrecht.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
    }
}

DATABASES['default']['NAME'] = get_secret(
    'DATABASES_NAME', default=DATABASES['default']['NAME'])
DATABASES['default']['USER'] = get_secret(
    'DATABASES_USER', default=DATABASES['default']['USER'])
DATABASES['default']['PASSWORD'] = get_secret(
    'DATABASES_PASSWORD', default=DATABASES['default']['PASSWORD'])


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'nl-NL'

TIME_ZONE = 'Europe/Amsterdam'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Mail settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_PASSWORD = get_secret('EMAIL_HOST_PASSWORD')
EMAIL_HOST_USER = get_secret('EMAIL_HOST_USER')
DEFAULT_FROM_EMAIL = get_secret('DEFAULT_FROM_EMAIL')
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
MEDIA_ROOT = path.normpath(path.join(PROJECT_DIR, 'media'))
MEDIA_URL = '/media/'

STATIC_ROOT = path.normpath(path.join(PROJECT_DIR, 'static'))
STATIC_URL = '/static/'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

PREPEND_WWW = True

CRISPY_TEMPLATE_PACK = 'bootstrap3'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': path.normpath(path.join(BASE_DIR, 'tvdordrecht.log')),
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
