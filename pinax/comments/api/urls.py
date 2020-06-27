from django.urls import path
from rest_framework import routers

from rest_framework.schemas import get_schema_view

from pinax.comments.api import views

router = routers.SimpleRouter()
router.register('comments', views.CommentViewSet, basename='comment')

comments_urlpatterns = [
    # add extras here
] + router.urls


openapi_routes = path(
    "openapi",
    get_schema_view(
        title="Pinax Comments",
        description="Api for Pinax Comments",
        version="0.0.1",
        patterns=comments_urlpatterns,
    ),
    name="openapi-schema",
)

urlpatterns = comments_urlpatterns + [openapi_routes]
