from __future__ import unicode_literals

from django import template
from django.core.urlresolvers import reverse

from django.contrib.contenttypes.models import ContentType

from ..authorization import load_can_delete, load_can_edit
from ..forms import CommentForm
from ..models import Comment


can_delete = load_can_delete()
can_edit = load_can_edit()
register = template.Library()


@register.filter
def can_edit_comment(comment, user):
    return can_edit(user, comment)


@register.filter
def can_delete_comment(comment, user):
    return can_delete(user, comment)


class BaseCommentNode(template.Node):

    @classmethod
    def handle_token(cls, parser, token):
        bits = token.split_contents()
        if not cls.requires_as_var and len(bits) == 2:
            return cls(parser.compile_filter(bits[1]))
        elif len(bits) == 4:
            if bits[2] != "as":
                raise template.TemplateSyntaxError("%r's 2nd argument must be 'as'" % bits[0])
            return cls(parser.compile_filter(bits[1]), bits[3])
        if cls.requires_as_var:
            args = "1 argument"
        else:
            args = "either 1 or 3 arguments"
        raise template.TemplateSyntaxError("%r takes %s" % (bits[0], args))

    def __init__(self, obj, varname=None):
        self.obj = obj
        self.varname = varname

    def get_comments(self, context):
        obj = self.obj.resolve(context)
        comments = Comment.objects.filter(
            object_id=obj.pk,
            content_type=ContentType.objects.get_for_model(obj)
        )
        return comments.order_by("submit_date")


class CommentCountNode(BaseCommentNode):

    requires_as_var = False

    def render(self, context):
        comments = self.get_comments(context).count()
        if self.varname is not None:
            context[self.varname] = comments
            return ""
        return comments


class CommentsNode(BaseCommentNode):

    requires_as_var = True

    def render(self, context):
        context[self.varname] = self.get_comments(context)
        return ""


class CommentFormNode(BaseCommentNode):

    requires_as_var = False

    def render(self, context):
        obj = self.obj.resolve(context)
        user = context.get("user")
        form_class = context.get("form", CommentForm)
        form = form_class(obj=obj, user=user)
        context[self.varname] = form
        return ""


class CommentTargetNode(BaseCommentNode):

    requires_as_var = False

    def render(self, context):
        obj = self.obj.resolve(context)
        return reverse("post_comment", kwargs={
            "content_type_id": ContentType.objects.get_for_model(obj).pk,
            "object_id": obj.pk
        })


@register.tag
def comment_count(parser, token):
    """
    Usage:

        {% comment_count obj %}
    or
        {% comment_count obj as var %}
    """
    return CommentCountNode.handle_token(parser, token)


@register.tag
def comments(parser, token):
    """
    Usage:

        {% comments obj as var %}
    """
    return CommentsNode.handle_token(parser, token)


@register.tag
def comment_form(parser, token):
    """
    Usage:

        {% comment_form obj as comment_form %}

    Will read the `user` var out of the contex to know if the form should be
    form an auth'd user or not.
    """
    return CommentFormNode.handle_token(parser, token)


@register.tag
def comment_target(parser, token):
    """
    Usage:

        {% comment_target obj [as varname] %}
    """
    return CommentTargetNode.handle_token(parser, token)
