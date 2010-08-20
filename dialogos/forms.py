from django import forms

from django.contrib.contenttypes.models import ContentType

from dialogos.models import Comment


class BaseCommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        self.obj = kwargs.pop("obj")
        super(BaseCommentForm, self).__init__(*args, **kwargs)
    
    def save(self, commit=True):
        comment = super(BaseCommentForm, self).save(commit=False)
        comment.ip_address = self.request.META.get("REMOTE_ADDR", None)
        comment.content_type = ContentType.objects.get_for_model(self.obj)
        comment.object_id = self.obj.pk
        if commit:
            comment.save()
        return comment



class UnauthenticatedCommentForm(BaseCommentForm):
    class Meta:
        model = Comment
        fields = [
            "name", "email", "website", "comment"
        ]
