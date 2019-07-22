import os
import re

BASEDIR = 'application'

ENV = 'development' # Turns on debugging features in Flask
DEBUG = True

WEBPACK_LOADER = {
    'BUNDLE_DIR_NAME': os.path.join(BASEDIR, 'public'),
    'STATIC_URL': 'static',
    'STATS_FILE': os.path.join(BASEDIR, 'webpack-stats.json'),
    'POLL_INTERVAL': 0.1,
    'TIMEOUT': None,
    'IGNORES': [re.compile(r'.+\.hot-update.js'), re.compile(r'.+\.map')]
}