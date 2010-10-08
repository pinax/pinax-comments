from datetime import datetime

from django.db import models

from django.contrib.auth.models import User
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Comment(models.Model):
    
    author = models.ForeignKey(User, null=True, related_name="comments")
    
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=255, blank=True)
    website = models.CharField(max_length=255, blank=True)
    
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField()
    content_object = GenericForeignKey()
    
    comment = models.TextField()
    
    submit_date = models.DateTimeField(default=datetime.now)
    ip_address = models.IPAddressField(null=True)
    public = models.BooleanField(default=True)
    
    def __unicode__(self):
        return "pk=%d" % self.pk
