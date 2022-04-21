from .base import *  # noqa: F403


DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [  # noqa: F405
    'debug_toolbar',
]

MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')  # noqa: F405,E501
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INTERNAL_IPS = [
    'localhost',
    '127.0.0.1',
]
