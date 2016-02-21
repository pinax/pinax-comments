# pinax-comments

`pinax-comments` is a comments app for Django.

!!! note "Pinax Ecosystem"
    This app was developed as part of the Pinax ecosystem but is just a Django app
    and can be used independently of other Pinax apps.
    
    To learn more about Pinax, see <http://pinaxproject.com/>


## Quickstart

Install the development version:

    pip install pinax-comments

Add `pinax.comments` to your `INSTALLED_APPS` setting:

    INSTALLED_APPS = (
        # ...
        "pinax.comments",
        # ...
    )

Add entry to your `urls.py`:

    url(r"^comments/", include("pinax.comments.urls"))
