from __future__ import unicode_literals

from appconf import AppConf
from django.conf import settings  # noqa
from django.core.exceptions import ImproperlyConfigured
import importlib


def load_path_attr(path):
    i = path.rfind(".")
    module, attr = path[:i], path[i + 1:]
    try:
        mod = importlib.import_module(module)
    except ImportError as e:
        raise ImproperlyConfigured("Error importing {0}: '{1}'".format(module, e))
    try:
        attr = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured("Module '{0}' does not define a '{1}'".format(module, attr))
    return attr


class CommentsAppConf(AppConf):
    CAN_DELETE_CALLABLE = "pinax.comments.authorization.default_can_delete"
    CAN_EDIT_CALLABLE = "pinax.comments.authorization.default_can_edit"

    def configure_can_delete_callable(self, value):
        return load_path_attr(value)

    def configure_can_edit_callable(self, value):
        return load_path_attr(value)
