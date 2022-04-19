import sys
from .base import *


DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [  # noqa: F405
    'debug_toolbar',
]

MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')  # noqa: F405,E501
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Cache
if 'test' in sys.argv:
    CACHE_TTL = 0
    for cache_name in CACHES.keys():  # noqa: F405
        CACHES[cache_name]['BACKEND'] = 'django.core.cache.backends.dummy.DummyCache'  # noqa: F405,E501
else:
    CACHE_TTL = 999

INTERNAL_IPS = [
    'localhost',
    '127.0.0.1',
]
