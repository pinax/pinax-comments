import pkg_resources


default_app_config = "pinax.comments.apps.AppConfig"
__version__ = pkg_resources.get_distribution("pinax-comments").version
