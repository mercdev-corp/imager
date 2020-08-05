import os, sys

from split_settings.tools import optional, include


include(
    'rest.py',
    'main.py',
    'connections.py',
    'apps.py',
    'celery.py',

    scope=locals()
)

if os.environ.get('DOCKER_CONTAINER'):
    include(
        'docker.py',

        scope=locals()
    )

if 'test' in sys.argv or 'test_coverage' in sys.argv:
    include(
        optional('test.py'),

        scope=locals()
    )

if not os.environ.get('DOCKER_CONTAINER'):
    include(
        optional('../settings_local.py'),

        scope=locals()
    )
