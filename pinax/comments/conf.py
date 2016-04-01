from __future__ import unicode_literals


from django.conf import settings

from appconf import AppConf


class CommentsAppConf(AppConf):

    COMMENTS_CAN_DELETE_CALLABLE = True
    COMMENTS_CAN_EDIT_CALLABLE = True