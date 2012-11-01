from django import forms

from django.contrib.contenttypes.models import ContentType

from dialogos.models import Comment


class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = [
            "name", "email", "website", "comment"
        ]
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        self.obj = kwargs.pop("obj")
        self.user = kwargs.pop("user")
        super(CommentForm, self).__init__(*args, **kwargs)
        if self.user is not None and not self.user.is_anonymous():
            del self.fields["name"]
            del self.fields["email"]
            del self.fields["website"]
    
    def save(self, commit=True):
        comment = super(CommentForm, self).save(commit=False)
        comment.ip_address = self.request.META.get("REMOTE_ADDR", None)
        comment.content_type = ContentType.objects.get_for_model(self.obj)
        comment.object_id = self.obj.pk
        if self.user is not None and not self.user.is_anonymous():
            comment.author = self.user
        if commit:
            comment.save()
        return comment
