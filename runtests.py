#!/usr/bin/env python

import os
import sys
import django
from django.conf import settings


def delete_migrations():
    from os.path import exists, abspath, dirname, join
    migrations_dir = join(
            dirname(abspath(__file__)), 'common', 'tests', 'migrations')
    if exists(migrations_dir):
        os.system('rm -r ' + migrations_dir)


def main():
    import warnings
    warnings.filterwarnings('error', category=DeprecationWarning)

    delete_migrations()

    if not settings.configured:
        # Dynamically configure the Django settings with the minimum necessary to
        # get Django running tests
        settings.configure(
                INSTALLED_APPS=[
                    'common',
                    'common.tests',
                ],
                DATABASES={
                    'default': {
                        'ENGINE': 'django.db.backends.sqlite3',
                    }
                },
        )

    django.setup()

    from django.test.utils import get_runner
    test_runner = get_runner(settings)(verbosity=2, interactive=True)
    if '--failfast' in sys.argv:
        test_runner.failfast = True

    failures = test_runner.run_tests(['common'])

    delete_migrations()

    sys.exit(failures)

if __name__ == '__main__':
    main()
