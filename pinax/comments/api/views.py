from rest_framework import viewsets
from pinax.comments.models import Comment
from pinax.comments.api import serializers


class CommentViewSet(viewsets.ModelViewSet):
    model = Comment
    serializer_class = serializers.CommentSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CommentInternalPrivateSerializer
        return self.serializer_class