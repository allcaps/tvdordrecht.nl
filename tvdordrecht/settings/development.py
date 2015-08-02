from settings.base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
EMAIL_HOST = 'localhost'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ALLOWED_HOSTS = ['127.0.0.1', ]

INSTALLED_APPS += [
 #   'debug_toolbar',
]

# http://django-debug-toolbar.readthedocs.org/en/latest/installation.html
INTERNAL_IPS = ('127.0.0.1', )

PREPEND_WWW = False
