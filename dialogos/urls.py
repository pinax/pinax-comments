from django.conf.urls import url, patterns


urlpatterns = patterns("dialogos.views",
    url(r"^comment/(?P<content_type_id>\d+)/(?P<object_id>\d+)/$", "post_comment",
        name="post_comment"),
    url(r"^comment/(?P<comment_id>\d+)/delete/$", "delete_comment",
        name="delete_comment"),
    url(r"^comment/(?P<comment_id>\d+)/edit/$", "edit_comment",
        name="edit_comment")
)
