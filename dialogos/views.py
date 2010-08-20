from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect

from django.contrib.contenttypes.models import ContentType

from dialogos.forms import UnauthenticatedCommentForm


@require_POST
def post_comment(request, content_type_id, object_id):
    content_type = get_object_or_404(ContentType, pk=content_type_id)
    obj = get_object_or_404(content_type.model_class(), pk=object_id)
    if request.user.is_authenticated():
        raise NotImplemented
    else:
        form_class = UnauthenticatedCommentForm
    form = form_class(request.POST, request=request, obj=obj)
    if not form.is_valid():
        raise NotImplemented
    form.save()
    return redirect(obj)
