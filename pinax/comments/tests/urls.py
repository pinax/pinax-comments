from django.conf.urls import include, url
from django.views.generic import TemplateView


urlpatterns = [
    url(r"^", include("pinax.comments.urls")),
    url(r"^demo/$", TemplateView.as_view(), name="demo_detail"),
]
