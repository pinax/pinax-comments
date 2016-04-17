from django.core.urlresolvers import reverse
from django.template import Template, Context

from django.contrib.contenttypes.models import ContentType

from pinax.comments.forms import CommentForm
from pinax.comments.models import Comment

from .models import Demo
from .test import TestCase


class TestCaseMixin(TestCase):
    def get(self, url_name, *args, **kwargs):
        data = kwargs.pop("data", {})
        return self.get(reverse(url_name, args=args, kwargs=kwargs), data)

    def getajax(self, url_name, *args, **kwargs):
        data = kwargs.pop("data", {})
        return self.get(reverse(url_name, args=args, kwargs=kwargs), data,
                        HTTP_X_REQUESTED_WITH="XMLHttpRequest")

    def post_comment_2(self, url_name, *args, **kwargs):
        url_name = "pinax_comments:" + url_name
        return self.post(url_name, args=args, kwargs=kwargs)

    def postajax(self, url_name, *args, **kwargs):
        data = kwargs.pop("data", {})
        return self.post(reverse(url_name, args=args, kwargs=kwargs), data,
                         HTTP_X_REQUESTED_WITH="XMLHttpRequest")

    def reload(self, obj):
        return obj.__class__._default_manager.get(pk=obj.pk)

    def assert_renders(self, tmpl, context, value):
        tmpl = Template(tmpl)
        self.assertEqual(tmpl.render(context), value)


class CommentTests(TestCaseMixin):
    def setUp(self):
        super(CommentTests, self).setUp()
        self.gimli = self.make_user(username="gimli")
        self.aragorn = self.make_user(username="aragorn")

    def assert_renders(self, tmpl, context, value):
        tmpl = Template(tmpl)
        self.assertEqual(tmpl.render(context), value)

    def post_comment(self, obj, data):
        return self.post(
            "pinax_comments:post_comment",
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
        self.response_302(response)

        self.assertEqual(Comment.objects.count(), 1)
        c = Comment.objects.get()
        self.assertEqual(c.author, None)
        self.assertEqual(c.name, "Frodo Baggins")

        response = self.post_comment(d, data={
            "comment": "Where is everyone?"
        })
        self.assertEqual(Comment.objects.count(), 1)

        with self.login(self.gimli):
            response = self.post_comment(d, data={
                "comment": "I thought you were watching the hobbits?"
            })
            self.response_302(response)
            self.assertEqual(Comment.objects.count(), 2)

            c = Comment.objects.order_by("id")[1]
            self.assertEqual(c.comment, "I thought you were watching the hobbits?")
            self.assertEqual(c.author, self.gimli)

    def test_delete_comment(self):
        d = Demo.objects.create(name="Wizard")
        with self.login(self.gimli):
            response = self.post_comment(d, data={
                "comment": "Wow, you're a jerk.",
            })
            comment = Comment.objects.get()
        response = self.post("pinax_comments:delete_comment", pk=comment.pk)
        self.response_404(response)
        self.assertEqual(Comment.objects.count(), 1)

        with self.login(self.aragorn):
            response = self.post("pinax_comments:delete_comment", pk=comment.pk)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(Comment.objects.count(), 1)

        with self.login(self.gimli):
            response = self.post("pinax_comments:delete_comment", pk=comment.pk)
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

    with self.login(self.gimli):
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
