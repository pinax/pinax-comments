from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from eldarion.test import TestCase

from dialogos.models import Comment


class CommentTests(TestCase):
    def test_post_comment(self):
        g = User.objects.create(username="Gandalf")
        
        response = self.post("post_comment", 
            content_type_id=ContentType.objects.get_for_model(g).pk,
            object_id=g.pk,
            data={
                "name": "Frodo Baggins",
                "comment": "Where'd you go?",
            }
        )
        self.assertEqual(response.status_code, 302)
        
        self.assertEqual(Comment.objects.count(), 1)
        c = Comment.objects.get()
        self.assertEqual(c.author, None)
        self.assertEqual(c.name, "Frodo Baggins")
