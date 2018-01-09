class CommentsDefaultHookSet(object):

    def load_can_delete(self, user, comment):
        if user.is_superuser:
            return True
        return user == comment.author

    def load_can_edit(self, user, comment):
        return user == comment.author


class HookProxy(object):
    def __getattr__(self, attr):
        from .conf import settings
        return getattr(settings.COMMENTS_HOOKSET, attr)


hookset = HookProxy()
