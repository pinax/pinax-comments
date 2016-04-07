from .conf import settings


def default_can_delete(user, comment):
    if user.is_superuser:
        return True
    return user == comment.author


def default_can_edit(user, comment):
    return user == comment.author


def load_can_delete():
    import_path = settings.COMMENTS_CAN_EDIT_CALLABLE

    if import_path is None:
        return default_can_delete


def load_can_edit():
    import_path = settings.COMMENTS_CAN_EDIT_CALLABLE

    if import_path is None:
        return default_can_edit
