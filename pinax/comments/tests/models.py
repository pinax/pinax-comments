from django.core.urlresolvers import reverse
from django.db import models


class Demo(models.Model):
    name = models.CharField(max_length=10)

    def get_absolute_url(self):
        return reverse("demo_detail")
