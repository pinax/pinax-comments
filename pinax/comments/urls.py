from django.conf.urls import url

from . import views

app_name = "pinax_comments"

urlpatterns = [
    url(r"^(?P<content_type_id>\d+)/(?P<object_id>\d+)/$", views.CommentCreateView.as_view(), name="post_comment"),
    url(r"^(?P<pk>\d+)/delete/$", views.CommentDeleteView.as_view(), name="delete_comment"),
    url(r"^(?P<pk>\d+)/edit/$", views.CommentUpdateView.as_view(), name="edit_comment"),
]
