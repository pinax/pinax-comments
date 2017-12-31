from django.db import models
from django.urls import reverse


class Demo(models.Model):
    name = models.CharField(max_length=10)

    def get_absolute_url(self):
        return reverse("demo_detail")
