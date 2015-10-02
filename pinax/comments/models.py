from datetime import datetime

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


@python_2_unicode_compatible
class Comment(models.Model):

    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name="comments")

    name = models.CharField(max_length=100)
    email = models.CharField(max_length=255, blank=True)
    website = models.CharField(max_length=255, blank=True)

    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField()
    content_object = GenericForeignKey()

    comment = models.TextField()

    submit_date = models.DateTimeField(default=datetime.now)
    ip_address = models.GenericIPAddressField(null=True)
    public = models.BooleanField(default=True)

    def __str__(self):
        return "pk=%d" % self.pk
