![](http://pinaxproject.com/pinax-design/patches/pinax-comments.svg)


# Pinax Comments

[![](https://img.shields.io/pypi/v/pinax-comments.svg)](https://pypi.python.org/pypi/pinax-comments/)

[![CircleCi](https://img.shields.io/circleci/project/github/pinax/pinax-comments.svg)](https://circleci.com/gh/pinax/pinax-comments)
[![Codecov](https://img.shields.io/codecov/c/github/pinax/pinax-comments.svg)](https://codecov.io/gh/pinax/pinax-comments)
[![](https://img.shields.io/github/contributors/pinax/pinax-comments.svg)](https://github.com/pinax/pinax-comments/graphs/contributors)
[![](https://img.shields.io/github/issues-pr/pinax/pinax-comments.svg)](https://github.com/pinax/pinax-comments/pulls)
[![](https://img.shields.io/github/issues-pr-closed/pinax/pinax-comments.svg)](https://github.com/pinax/pinax-comments/pulls?q=is%3Apr+is%3Aclosed)

[![](http://slack.pinaxproject.com/badge.svg)](http://slack.pinaxproject.com/)
[![](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)


## Table of Contents

* [About Pinax](#about-pinax)
* [Overview](#overview)
  * [Supported Django and Python versions](#supported-django-and-python-versions)
* [Documentation](#documentation)
  * [Installation](#installation)
  * [Usage](#usage)
    * [Settings](#settings)
  * [Template Tags](#template-tags)
  * [Signals](#signals)
  * [Hookset Methods](#hookset-methods)
  * [Settings](#settings)
* [Change Log](#change-log)
* [Contribute](#contribute)
* [Code of Conduct](#code-of-conduct)
* [Connect with Pinax](#connect-with-pinax)
* [License](#license)


## About Pinax

Pinax is an open-source platform built on the Django Web Framework. It is an ecosystem of reusable
Django apps, themes, and starter project templates. This collection can be found at http://pinaxproject.com.


## pinax-comments

### Overview

`pinax-comments` is a comments app for Django.

#### Supported Django and Python versions

Django \ Python | 2.7 | 3.4 | 3.5 | 3.6
--------------- | --- | --- | --- | ---
1.11 |  *  |  *  |  *  |  *  
2.0  |     |  *  |  *  |  *


## Documentation

### Installation

Install the development version:

```shell
    $ pip install pinax-comments
```

Add `pinax.comments` to your `INSTALLED_APPS` setting:

```python
    INSTALLED_APPS = [
        # other apps
        "pinax.comments",
    ]
```

Add `pinax.comments.urls` to your project urlpatterns:

```python
    urlpatterns = [
        # other urls
        url(r"^comments/", include("pinax.comments.urls", namespace="pinax_comments"))
    ]
```

### Usage
    
Common usage involves wiring up template tags as seen in this example, which presents
a form for adding a new comment on `wall_user`, as well as showing existing comments.

Three template tags are used here: `comment_target`, which returns a URL for posting
a comment on `wall_user`; `comment_form`, which returns a comment form for
`wall_user`; and `comments`, which returns all comments on `wall_user`.

```django
    <div class="list-group">
        <div class="list-group-item">
            {% comment_target wall_user as post_url %}
            {% comment_form wall_user as comment_form %}
            <form class="form" method="post" action="{{ post_url }}">
                {% csrf_token %}
                {{ comment_form|bootstrap }}
                <button class="btn btn-primary">Post Message</button>
            </form>
        </div>
        
        {% comments wall_user as wall_comments %}
        {% for comment in wall_comments %}
        <div class="list-group-item">
            {{ comment.comment|linebreaks }}
            <div class="meta">
                <small class="text-muted pull-right">{{ comment.submit_date }}</small>
                <small class="text-muted">
                    <a href="{% url "wall" comment.author.username %}">
                        {{ comment.author }}
                    </a>
                </small>
            </div>
        </div>
        {% endfor %}
    </div>
```

### Template Tags

#### `can_delete_comment`

Returns True if `user` can delete `comment`.

```django
    {% if comment|can_delete_comment:user %}
```

#### `can_edit_comment`

Returns True if `user` can edit `comment`.

```django
    {% if comment|can_edit_comment:user %}
```

#### `comment_count`

Returns number of comments on `obj`.

Usage:

```django
    {% comment_count obj %}
```

or

```django
    {% comment_count obj as var %}
```

#### `comment_form`

Returns a comment form for `obj`. Checks context user to determine
if the comment should be from an authenticated or anonymous user. 

Usage:

```django
    {% comment_form obj as comment_form %}
```

#### `comment_target`

Returns the URL for posting a comment on `obj`

```django
    {% comment_target obj %}
```

or

```django
    {% comment_target obj as var %}
```

#### `comments`

Returns iterable of comments on `obj` as context variable `var`.

```django
    {% comments obj as var %}
```

### Signals

Both signals provide two keyword arguments: `comment`, the relevant `Comment` instance, and `request`.

#### `commented`

Sent when a comment is added. 

#### `comment_updated`

Sent when a comment is updated.

### Hookset Methods

#### `load_can_delete(self, user, comment)`
  
Override this method to specify if `user` can delete `comment`. By default only comment authors can edit comments.
  
#### `load_can_edit(self, user, comment)`
  
Override this method to specify if `user` can edit `comment`. By default, Django superusers and comment authors can delete comments.

This example hooks.py overrides default `load_can_edit()` with a silly alternative:

```python
# myapp.hooks.py

from pinax.comments.hooks import CommentsDefaultHookSet

class CommentsHookSet(CommentsDefaultHookSet):

    def load_can_edit(self, user, comment):
        return user.username in ["funk", "wagnalls"]
```

### Settings

#### PINAX_COMMENTS_HOOKSET

Used to provide your own custom hookset methods, as described above. Value is a dotted path to
your own hookset class:

```python
PINAX_COMMENTS_HOOKSET = "myapp.hooks.CommentsHookSet"
```

## Change Log

### 1.0.2

* Replace deprecated render_to_string() `context_instance` kwarg
* Add view tests
* Add templatetag tests

### 1.0.1

* add django>=1.11 requirement
* update testing requirements
* improve documentation markup
* remove "static" and "templates" dirs from MANIFEST.in

### 1.0.0

* Add Django 2.0 compatibility testing
* Drop Django 1.9, 1.9, 1.10 and Python 3.3 support
* Move documentation into README, standardize documentation layout
* Convert CI and coverage to CircleCi and CodeCov
* Add PyPi-compatible long description
* Add documentation for templatetags and signals
* Add usage example

### 0.1

* initial release


## Contribute

For an overview on how contributing to Pinax works read this [blog post](http://blog.pinaxproject.com/2016/02/26/recap-february-pinax-hangout/)
and watch the included video, or read our [How to Contribute](http://pinaxproject.com/pinax/how_to_contribute/) section.
For concrete contribution ideas, please see our
[Ways to Contribute/What We Need Help With](http://pinaxproject.com/pinax/ways_to_contribute/) section.

In case of any questions we recommend you join our [Pinax Slack team](http://slack.pinaxproject.com)
and ping us there instead of creating an issue on GitHub. Creating issues on GitHub is of course
also valid but we are usually able to help you faster if you ping us in Slack.

We also highly recommend reading our blog post on [Open Source and Self-Care](http://blog.pinaxproject.com/2016/01/19/open-source-and-self-care/).


## Code of Conduct

In order to foster a kind, inclusive, and harassment-free community, the Pinax Project
has a [code of conduct](http://pinaxproject.com/pinax/code_of_conduct/).
We ask you to treat everyone as a smart human programmer that shares an interest in Python, Django, and Pinax with you.


## Connect with Pinax

For updates and news regarding the Pinax Project, please follow us on Twitter [@pinaxproject](https://twitter.com/pinaxproject)
and check out our [Pinax Project blog](http://blog.pinaxproject.com).


## License

Copyright (c) 2012-2018 James Tauber and contributors under the [MIT license](https://opensource.org/licenses/MIT).
