from django.conf.urls import include, url
from django.views.generic import TemplateView

urlpatterns = [
    url(r"^comment/", include("pinax.comments.urls", namespace="pinax_comments")),
    url(r"^demo/$", TemplateView.as_view(), name="demo_detail"),
]
