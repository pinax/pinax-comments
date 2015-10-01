from django.core.urlresolvers import reverse
from django.db import models


@python_2_unicode_compatible
class Demo(models.Model):
    name = models.CharField(max_length=10)

    def get_absolute_url(self):
        return reverse("demo_detail")
