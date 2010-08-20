from django import template

from django.contrib.contenttypes.models import ContentType

from dialogos.models import Comment


register = template.Library()


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
        return Comment.objects.filter(
            object_id=obj.pk,
            content_type=ContentType.objects.get_for_model(obj)
        )

class CommentCountNode(BaseCommentNode):
    requires_as_var = False
    
    def render(self, context):
        comments = self.get_comments(context).count()
        if self.varname is not None:
            context[self.varname] = comments
            return ""
        return unicode(comments)


class CommentsNode(BaseCommentNode):
    requires_as_var = True
    
    def render(self, context):
        context[self.varname] = self.get_comments(context)
        return ""


@register.tag
def get_comment_count(parser, token):
    """
    Usage:
        
        {% get_comment_count obj %}
    or
        {% get_comment_count obj as var %}
    """
    return CommentCountNode.handle_token(parser, token)

@register.tag
def get_comments(parser, token):
    """
    Usage:
        
        {% get_comments obj as var %}
    """
    return CommentsNode.handle_token(parser, token)
