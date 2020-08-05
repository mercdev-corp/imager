CELERY_BROKER_URL = 'amqp://localhost:5672//'
CELERY_RESULT_BACKEND = CELERY_BROKER_URL

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'imager-postgres',
        'USER': 'imager-postgres',
        'PASSWORD': 'imager-postgres',
        'HOST': '127.0.0.1',
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'imager_cache_table',
    }
}
