# -*- coding: utf-8 -*-
#
# Copyright © 2012 - 2017 Michal Čihař <michal@cihar.com>
#
# This file is part of Weblate <https://weblate.org/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

#
# Django settings for running testsuite
#

import warnings
import os

from weblate.settings_example import *  # noqa

if 'CI_DATABASE' in os.environ:
    if os.environ['CI_DATABASE'] == 'mysql':
        DATABASES['default']['ENGINE'] = 'django.db.backends.mysql'
        DATABASES['default']['NAME'] = 'weblate'
        DATABASES['default']['USER'] = 'root'
        DATABASES['default']['PASSWORD'] = ''
        DATABASES['default']['OPTIONS'] = {
            'init_command': 'SET NAMES utf8, wait_timeout=28800',
        }
    elif os.environ['CI_DATABASE'] == 'postgresql':
        DATABASES['default']['ENGINE'] = \
            'django.db.backends.postgresql_psycopg2'
        DATABASES['default']['NAME'] = 'weblate'
        DATABASES['default']['USER'] = 'postgres'
        DATABASES['default']['PASSWORD'] = ''


# Configure admins
ADMINS = (('Weblate test', 'noreply@weblate.org'), )

# Different root for test repos
DATA_DIR = os.path.join(BASE_DIR, '..', 'data-test')

# Silent logging setup
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'weblate': {
            'handlers': [],
            'level': 'ERROR',
        },
        'social': {
            'handlers': [],
            'level': 'ERROR',
        },
    }
}

# Selenium can not clear HttpOnly cookies in MSIE
SESSION_COOKIE_HTTPONLY = False

# Test optional apps as well
INSTALLED_APPS += (
    'weblate.billing',
    'weblate.gitexport',
)

# Test GitHub auth
AUTHENTICATION_BACKENDS = (
    'weblate.accounts.auth.EmailAuth',
    'social_core.backends.github.GithubOAuth2',
    'weblate.accounts.auth.WeblateUserBackend',
)

warnings.filterwarnings(
    'error', r"DateTimeField .* received a naive datetime",
    RuntimeWarning, r'django\.db\.models\.fields'
)
