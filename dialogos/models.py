from datetime import datetime

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _


COMMENT_MAX_LENGTH = getattr(settings,'DIALOGOS_COMMENT_MAX_LENGTH', 3000)


class Comment(models.Model):
    
    author = models.ForeignKey(User, null=True, blank=True, related_name="comments")
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    website = models.CharField(max_length=50, null=True, blank=True)
    
    content_type = models.ForeignKey(ContentType, related_name="content_type_set_for_%(class)s")
    object_pk = models.TextField(_("object ID"))
    content_object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_pk")
    
    comment = models.TextField(_("comment"), max_length=COMMENT_MAX_LENGTH)
    
    submit_date = models.DateTimeField(_("date/time submitted"), default=datetime.now)
    ip_address = models.IPAddressField(_("IP address"), blank=True, null=True)
    is_public = models.BooleanField(_("is public"), default=True)
    is_removed = models.BooleanField(_("is removed"), default=False)

