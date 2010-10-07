from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType

from dialogos.forms import UnauthenticatedCommentForm, AuthenticatedCommentForm
from dialogos.models import Comment


@require_POST
def post_comment(request, content_type_id, object_id):
    content_type = get_object_or_404(ContentType, pk=content_type_id)
    obj = get_object_or_404(content_type.model_class(), pk=object_id)
    if request.user.is_authenticated():
        form_class = AuthenticatedCommentForm
    else:
        form_class = UnauthenticatedCommentForm
    form = form_class(request.POST, request=request, obj=obj)
    if form.is_valid():
        form.save()
    return HttpResponseRedirect(obj.get_absolute_url())

@login_required
@require_POST
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    obj = comment.content_object
    if comment.author == request.user:
        comment.delete()
    return HttpResponseRedirect(obj.get_absolute_url())
