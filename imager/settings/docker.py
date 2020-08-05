import os



CELERY_BROKER_URL = 'amqp://{}:5672//'.format(os.environ.get('RABBIT_HOST'))
CELERY_RESULT_BACKEND = CELERY_BROKER_URL

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_USER'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'imager_cache_table',
    }
}

MEDIA_ROOT = os.path.normpath(os.path.join('/imager', 'media', 'uploads'))
STATIC_ROOT = os.path.normpath(os.path.join('/imager', 'media', 'static'))
