#!/usr/bin/env python
import os
import sys

from django.conf import settings


if not settings.configured:
    settings.configure(
        DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3"}},
        ROOT_URLCONF="dialogos.urls",
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "dialogos",
        ]
    )


from django.test.simple import DjangoTestSuiteRunner


def runtests(*test_args):
    if not test_args:
        test_args = ["dialogos"]
    parent = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, parent)
    suite = DjangoTestSuiteRunner(verbosity=1, interactive=True)
    failures = suite.run_tests(test_args)
    sys.exit(failures)


if __name__ == "__main__":
    runtests(*sys.argv[1:])
