from django.core.urlresolvers import reverse
from django.template import Template, Context
from django.test import TestCase

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from pinax.comments.forms import CommentForm
from pinax.comments.models import Comment

from .models import Demo


class login(object):
    def __init__(self, testcase, user, password):
        self.testcase = testcase
        success = testcase.client.login(username=user, password=password)
        self.testcase.assertTrue(
            success,
            "login with username=%r, password=%r failed" % (user, password)
        )

    def __enter__(self):
        pass

    def __exit__(self, *args):
        self.testcase.client.logout()


class TestCaseMixin(object):
    def get(self, url_name, *args, **kwargs):
        data = kwargs.pop("data", {})
        return self.client.get(reverse(url_name, args=args, kwargs=kwargs), data)

    def getajax(self, url_name, *args, **kwargs):
        data = kwargs.pop("data", {})
        return self.client.get(reverse(url_name, args=args, kwargs=kwargs), data,
                               HTTP_X_REQUESTED_WITH="XMLHttpRequest")

    def post(self, url_name, *args, **kwargs):
        data = kwargs.pop("data", {})
        return self.client.post(reverse(url_name, args=args, kwargs=kwargs), data)

    def postajax(self, url_name, *args, **kwargs):
        data = kwargs.pop("data", {})
        return self.client.post(reverse(url_name, args=args, kwargs=kwargs), data,
                                HTTP_X_REQUESTED_WITH="XMLHttpRequest")

    def login(self, user, password):
        return login(self, user, password)

    def reload(self, obj):
        return obj.__class__._default_manager.get(pk=obj.pk)

    def assert_renders(self, tmpl, context, value):
        tmpl = Template(tmpl)
        self.assertEqual(tmpl.render(context), value)


class CommentTests(TestCaseMixin, TestCase):

    def setUp(self):
        self.user = User.objects.create_user("gimli", "myaxe@dwarf.org", "gloin")
        self.user2 = User.objects.create_user("aragorn", "theking@gondor.gov", "strider")

    def assert_renders(self, tmpl, context, value):
        tmpl = Template(tmpl)
        self.assertEqual(tmpl.render(context), value)

    def post_comment(self, obj, data):
        return self.post(
            "post_comment",
            content_type_id=ContentType.objects.get_for_model(obj).pk,
            object_id=obj.pk,
            data=data
        )

    def test_post_comment(self):
        d = Demo.objects.create(name="Wizard")

        response = self.post_comment(d, data={
            "name": "Frodo Baggins",
            "comment": "Where'd you go?",
        })
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Comment.objects.count(), 1)
        c = Comment.objects.get()
        self.assertEqual(c.author, None)
        self.assertEqual(c.name, "Frodo Baggins")

        response = self.post_comment(d, data={
            "comment": "Where is everyone?"
        })
        self.assertEqual(Comment.objects.count(), 1)

        with self.login("gimli", "gloin"):
            response = self.post_comment(d, data={
                "comment": "I thought you were watching the hobbits?"
            })
            self.assertEqual(response.status_code, 302)
            self.assertEqual(Comment.objects.count(), 2)

            c = Comment.objects.order_by("id")[1]
            self.assertEqual(c.comment, "I thought you were watching the hobbits?")
            self.assertEqual(c.author, self.user)

    def test_delete_comment(self):
        d = Demo.objects.create(name="Wizard")
        with self.login("gimli", "gloin"):
            response = self.post_comment(d, data={
                "comment": "Wow, you're a jerk.",
            })
            comment = Comment.objects.get()

        response = self.post("delete_comment", comment_id=comment.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 1)

        with self.login("aragorn", "strider"):
            response = self.post("delete_comment", comment_id=comment.pk)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(Comment.objects.count(), 1)

        with self.login("gimli", "gloin"):
            response = self.post("delete_comment", comment_id=comment.pk)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(Comment.objects.count(), 0)

    def test_ttag_comment_count(self):
        d = Demo.objects.create(name="Wizard")
        self.post_comment(d, data={
            "name": "Gandalf",
            "comment": "You can't win",
        })
        self.post_comment(d, data={
            "name": "Gollum",
            "comment": "We wants our precious",
        })

        self.assert_renders(
            "{% load pinax_comments_tags %}{% comment_count o %}",
            Context({"o": d}),
            "2"
        )

    def test_ttag_comments(self):
        d = Demo.objects.create(name="Wizard")
        self.post_comment(d, data={
            "name": "Gandalf",
            "comment": "You can't win",
        })
        self.post_comment(d, data={
            "name": "Gollum",
            "comment": "We wants our precious",
        })

        c = Context({"o": d})
        self.assert_renders(
            "{% load pinax_comments_tags %}{% comments o as cs %}",
            c,
            ""
        )
        self.assertEqual(list(c["cs"]), list(Comment.objects.all()))

    def test_ttag_comment_form(self):
        d = Demo.objects.create(name="Wizard")
        c = Context({"o": d})
        self.assert_renders(
            "{% load pinax_comments_tags %}{% comment_form o as comment_form %}",
            c,
            ""
        )
        self.assertTrue(isinstance(c["comment_form"], CommentForm))

        with self.login("gimli", "gloin"):
            c = Context({"o": d, "user": self.user})
            self.assert_renders(
                "{% load pinax_comments_tags %}{% comment_form o as comment_form %}",
                c,
                ""
            )
            self.assertTrue(isinstance(c["comment_form"], CommentForm))

    def test_ttag_comment_target(self):
        d = Demo.objects.create(name="Wizard")
        self.assert_renders(
            "{% load pinax_comments_tags %}{% comment_target o %}",
            Context({"o": d}),
            "/comment/%d/%d/" % (ContentType.objects.get_for_model(d).pk, d.pk)
        )
