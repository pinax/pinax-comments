from django.conf.urls.defaults import url, patterns, include, handler404, handler500


urlpatterns = patterns("dialogos.views",
    url(r"^comment/(?P<content_type_id>\d+)/(?P<object_id>\d+)/$", "post_comment",
        name="post_comment"),
)
