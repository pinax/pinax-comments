from datetime import datetime

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Comment(models.Model):

    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name="comments", on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    email = models.CharField(max_length=255, blank=True)
    website = models.CharField(max_length=255, blank=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.IntegerField()
    content_object = GenericForeignKey()

    comment = models.TextField()

    submit_date = models.DateTimeField(default=datetime.now)
    ip_address = models.GenericIPAddressField(null=True)
    public = models.BooleanField(default=True)

    @property
    def data(self):
        return {
            "pk": self.pk,
            "comment": self.comment,
            "author": self.author.username if self.author else "",
            "name": self.name,
            "email": self.email,
            "website": self.website,
            "submit_date": str(self.submit_date)
        }

    def __str__(self):
        return "pk=%d" % self.pk  # pragma: no cover
