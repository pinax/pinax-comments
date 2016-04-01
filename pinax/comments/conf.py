from __future__ import unicode_literals

from appconf import AppConf
from django.conf import settings


class CommentsAppConf(AppConf):
    CAN_DELETE_CALLABLE = True
    CAN_EDIT_CALLABLE = True
