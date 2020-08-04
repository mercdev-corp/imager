import sys

from split_settings.tools import optional, include


include(
    'main.py',
    'apps.py',

    scope=locals()
)

if 'test' in sys.argv or'test_coverage' in sys.argv:
    include(
        optional('test.py'),

        scope=locals()
    )

include(
    optional('../settings_local.py'),

    scope=locals()
)
