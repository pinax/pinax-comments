from datetime import datetime

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _


class Comment(models.Model):
    
    author = models.ForeignKey(User, null=True, blank=True, related_name="comments")
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    website = models.CharField(max_length=50, null=True, blank=True)
    
    content_type = models.ForeignKey(ContentType, related_name="content_type_set_for_%(class)s")
    object_pk = models.TextField(_("object ID"))
    content_object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_pk")
    
    comment = models.TextField(_("comment"))
    
    submit_date = models.DateTimeField(_("date/time submitted"), default=datetime.now)
    ip_address = models.IPAddressField(_("IP address"), blank=True, null=True)
    is_public = models.BooleanField(_("is public"), default=True)
    is_removed = models.BooleanField(_("is removed"), default=False)


class CommentFlag(models.Model):
    
    user = models.ForeignKey(User, related_name="comment_flags")
    comment = models.ForeignKey(Comment, related_name="flags")
    flag = models.CharField(_("flag"), max_length=30, db_index=True)
    reason = models.IntegerField(_("reason"), choices=settings.COMMENT_FLAG_REASONS)
    flag_date = models.DateTimeField(_("date"), default=datetime.now)
    
