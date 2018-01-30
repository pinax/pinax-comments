from setuptools import find_packages, setup

VERSION = "1.0.2"
LONG_DESCRIPTION = """
.. image:: http://pinaxproject.com/pinax-design/patches/pinax-comments.svg
    :target: https://pypi.python.org/pypi/pinax-comments/

==============
Pinax Comments
==============

.. image:: https://img.shields.io/pypi/v/pinax-comments.svg
    :target: https://pypi.python.org/pypi/pinax-comments/

\ 

.. image:: https://img.shields.io/circleci/project/github/pinax/pinax-comments.svg
    :target: https://circleci.com/gh/pinax/pinax-comments
.. image:: https://img.shields.io/codecov/c/github/pinax/pinax-comments.svg
    :target: https://codecov.io/gh/pinax/pinax-comments
.. image:: https://img.shields.io/github/contributors/pinax/pinax-comments.svg
    :target: https://github.com/pinax/pinax-comments/graphs/contributors
.. image:: https://img.shields.io/github/issues-pr/pinax/pinax-comments.svg
    :target: https://github.com/pinax/pinax-comments/pulls
.. image:: https://img.shields.io/github/issues-pr-closed/pinax/pinax-comments.svg
    :target: https://github.com/pinax/pinax-comments/pulls?q=is%3Apr+is%3Aclosed

\ 

.. image:: http://slack.pinaxproject.com/badge.svg
    :target: http://slack.pinaxproject.com/
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://opensource.org/licenses/MIT/

\ 

``pinax-comments`` is a comments app for Django.
 
Supported Django and Python Versions
------------------------------------

+-----------------+-----+-----+-----+-----+
| Django / Python | 2.7 | 3.4 | 3.5 | 3.6 |
+=================+=====+=====+=====+=====+
|  1.11           |  *  |  *  |  *  |  *  |
+-----------------+-----+-----+-----+-----+
|  2.0            |     |  *  |  *  |  *  |
+-----------------+-----+-----+-----+-----+
"""

setup(
    author="Pinax Team",
    author_email="team@pinaxprojects.com",
    description="a comments app for Django",
    name="pinax-comments",
    long_description=LONG_DESCRIPTION,
    version=VERSION,
    url="http://github.com/pinax/pinax-comments/",
    license="MIT",
    packages=find_packages(),
    package_data={
        "comments": []
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        "django>=1.11",
        "django-appconf>=1.0.1",
    ],
    tests_require=[
        "django-test-plus>=1.0.22",
        "django-appconf>=1.0.1",
        "django-user-accounts>=2.0.3",
    ],
    test_suite="runtests.runtests",
    zip_safe=False
)
