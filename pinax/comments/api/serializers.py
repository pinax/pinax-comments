from rest_framework import serializers
from pinax.comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'pk',
            'name',
            'comment',
            'submit_date',
            'public',
            'author',
        ]

class CommentInternalPrivateSerializer(CommentSerializer):
    class Meta:
        model = Comment
        fields = CommentSerializer.Meta.fields + [
            'object_id',
            'content_type',
            'email',
            'website',
            'ip_address',
        ]
