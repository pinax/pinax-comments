Pinax Starter App
=================

.. image:: http://slack.pinaxproject.com/badge.svg
   :target: http://slack.pinaxproject.com/
   
.. image:: https://img.shields.io/travis/<user_or_org_name>/pinax-comments.svg
   :target: https://travis-ci.org/<user_or_org_name>/pinax-comments

.. image:: https://img.shields.io/coveralls/<user_or_org_name>/pinax-comments.svg
   :target: https://coveralls.io/r/<user_or_org_name>/pinax-comments

.. image:: https://img.shields.io/pypi/dm/pinax-comments.svg
   :target:  https://pypi.python.org/pypi/pinax-comments/

.. image:: https://img.shields.io/pypi/v/pinax-comments.svg
   :target:  https://pypi.python.org/pypi/pinax-comments/

.. image:: https://img.shields.io/badge/license-<license>-blue.svg
   :target:  https://pypi.python.org/pypi/pinax-comments/
   

Pinax
------

Pinax is an open-source platform built on the Django Web Framework. It is an ecosystem of reusable Django apps, themes, and starter project templates. 
This collection can be found at http://pinaxproject.com.


pinax-starter-app
------------------
   
``pinax-starter-app`` is a starter app template for Pinax apps.
   
Quickly setup the scaffolding for your django app.

What you get:

* test infrastructure
* Travis configuration with coveralls
* documentation instrastructure
* MIT LICENSE
* setup.py


Getting Started
----------------

Execute::

    pip install Django
    django-admin.py startapp --template=https://github.com/pinax/pinax-starter-app/zipball/master --extension=py,rst,in,sh,rc,yml,ini,coveragerc <project_name>


After you are running you have a fresh app, first update this readme by removing
everything above and including this line and unindenting everything below this line. Also
remember to edit the ``<user_or_org_name>`` in the travis and coveralls badge/links::


Running the Tests
-------------------

    ::

       $ pip install detox
       $ detox


Documentation
---------------

The Pinax documentation is available at http://pinaxproject.com/pinax/.


Code of Conduct
----------------

In order to foster a kind, inclusive, and harassment-free community, the Pinax Project has a code of conduct, which can be found here  http://pinaxproject.com/pinax/code_of_conduct/.


Pinax Project Blog and Twitter
--------------------------------

For updates and news regarding the Pinax Project, please follow us on Twitter at @pinaxproject and check out our blog http://blog.pinaxproject.com.
