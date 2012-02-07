from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect

from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType

from dialogos.forms import CommentForm
from dialogos.models import Comment
from dialogos.signals import commented


@require_POST
def post_comment(request, content_type_id, object_id):
    content_type = get_object_or_404(ContentType, pk=content_type_id)
    obj = get_object_or_404(content_type.model_class(), pk=object_id)
    form = CommentForm(request.POST, request=request, obj=obj, user=request.user)
    if form.is_valid():
        comment = form.save()
        commented.send(sender=post_comment, comment=comment, request=request)
    redirect_to = request.POST.get("next")
    # light security check -- make sure redirect_to isn't garbage.
    if not redirect_to or " " in redirect_to or redirect_to.startswith("http"):
        redirect_to = obj
    return redirect(redirect_to)


@login_required
@require_POST
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    obj = comment.content_object
    if comment.author == request.user:
        comment.delete()
    return redirect(obj)
