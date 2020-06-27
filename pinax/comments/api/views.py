from rest_framework import viewsets
from pinax.comments.models import Comment
from pinax.comments.api import serializers


class CommentViewSet(viewsets.ModelViewSet):
    model = Comment
    serializer_class = serializers.CommentSerializer
