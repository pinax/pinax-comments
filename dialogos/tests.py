from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from eldarion.test import TestCase

from dialogos.models import Comment


class CommentTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("gimli", "myaxe@dwarf.org", "gloin")
    
    def post_comment(self, obj, data):
        return self.post("post_comment",
            content_type_id=ContentType.objects.get_for_model(obj).pk,
            object_id=obj.pk,
            data=data
        )
    
    def test_post_comment(self):
        g = User.objects.create(username="Gandalf")
        
        response = self.post_comment(g, data={
            "name": "Frodo Baggins",
            "comment": "Where'd you go?",
        })
        self.assertEqual(response.status_code, 302)
        
        self.assertEqual(Comment.objects.count(), 1)
        c = Comment.objects.get()
        self.assertEqual(c.author, None)
        self.assertEqual(c.name, "Frodo Baggins")
        
        with self.login("gimli", "gloin"):
            response = self.post_comment(g, data={
                "comment": "I thought you were watching the hobbits?"
            })
            self.assertEqual(response.status_code, 302)
            self.assertEqual(Comment.objects.count(), 2)
            
            c = Comment.objects.order_by("id")[1]
            self.assertEqual(c.comment, "I thought you were watching the hobbits?")
            self.assertEqual(c.author, self.user)
