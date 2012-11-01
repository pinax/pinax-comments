from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
try:
    from django.utils.importlib import import_module
except ImportError:
    from importlib import import_module


def load_path_attr(path):
    i = path.rfind(".")
    module, attr = path[:i], path[i + 1:]
    try:
        mod = import_module(module)
    except ImportError, e:
        raise ImproperlyConfigured("Error importing %s: '%s'" % (module, e))
    try:
        attr = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured("Module '%s' does not define a '%s'" % (module, attr))
    return attr


def default_can_delete(user, comment):
    if user.is_superuser:
        return True
    return user == comment.author


def default_can_edit(user, comment):
    return user == comment.author


def load_can_delete():
    import_path = getattr(settings, "COMMENTS_CAN_DELETE_CALLABLE", None)
    
    if import_path is None:
        return default_can_delete
    
    return load_path_attr(import_path)


def load_can_edit():
    import_path = getattr(settings, "COMMENTS_CAN_EDIT_CALLABLE", None)
    
    if import_path is None:
        return default_can_edit
    
    return load_path_attr(import_path)
