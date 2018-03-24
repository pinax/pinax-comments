from django.contrib.contenttypes.models import ContentType
from django.template import Context, Template
from django.urls import reverse

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

    def post_ajax(self, url_name, *args, **kwargs):
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

    def post_comment(self, obj, data, **kwargs):
        return self.post(
            "pinax_comments:post_comment",
            content_type_id=ContentType.objects.get_for_model(obj).pk,
            object_id=obj.pk,
            data=data,
            **kwargs
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

    def test_ajax_post_comment(self):
        """Verify comment created via AJAX"""
        d = Demo.objects.create(name="Wizard")

        response = self.post_comment(d, data={
            "name": "Frodo Baggins",
            "comment": "Where'd you go?",
        }, extra=dict(HTTP_X_REQUESTED_WITH="XMLHttpRequest"))
        self.response_200(response)

        self.assertEqual(Comment.objects.count(), 1)
        c = Comment.objects.get()
        self.assertEqual(c.author, None)
        self.assertEqual(c.name, "Frodo Baggins")

    def test_ajax_post_comment_bad_data(self):
        """Verify no comment created if form data is invalid"""
        d = Demo.objects.create(name="Wizard")

        response = self.post_comment(d, data={
            "artist": "Frida Kahlo",
            "comment": "Where'd you go?",
        }, extra=dict(HTTP_X_REQUESTED_WITH="XMLHttpRequest"))
        self.response_200(response)
        # Ensure no comment was created
        self.assertEqual(Comment.objects.count(), 0)

    def test_update_comment(self):
        """Ensure existing comment is updated"""
        d = Demo.objects.create(name="Wizard")
        with self.login(self.gimli):
            response = self.post_comment(d, data={
                "comment": "Wow, you're a jerk.",
            })
            comment = Comment.objects.get()

            new_comment = "Oops, wrong wizard! You are wonderful!"
            post_data = dict(comment=new_comment)
            response = self.post(
                "pinax_comments:edit_comment",
                pk=comment.pk,
                data=post_data,
            )
            self.assertEqual(response.status_code, 302)
            comment.refresh_from_db()
            self.assertEqual(comment.comment, new_comment)

    def test_ajax_update_comment(self):
        """Ensure existing comment is updated"""
        d = Demo.objects.create(name="Wizard")
        with self.login(self.gimli):
            self.post_comment(d, data={
                "comment": "Wow, you're a jerk.",
            })
            comment = Comment.objects.get()

            new_comment = "Oops, wrong wizard! You are wonderful!"
            post_data = dict(comment=new_comment)
            response = self.post(
                "pinax_comments:edit_comment",
                pk=comment.pk,
                data=post_data,
                extra=dict(HTTP_X_REQUESTED_WITH="XMLHttpRequest")
            )
            self.assertEqual(response.status_code, 200)
            comment.refresh_from_db()
            self.assertEqual(comment.comment, new_comment)

    def test_delete_comment(self):
        d = Demo.objects.create(name="Wizard")
        with self.login(self.gimli):
            response = self.post_comment(d, data={
                "comment": "Wow, you're a jerk.",
            })
            comment = Comment.objects.get()

        # Anonymous user cannot delete
        response = self.post("pinax_comments:delete_comment", pk=comment.pk)
        self.response_302(response)
        self.assertEqual(Comment.objects.count(), 1)

        # User is not comment author, cannot delete
        with self.login(self.aragorn):
            response = self.post("pinax_comments:delete_comment", pk=comment.pk)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(Comment.objects.count(), 1)

        # Comment author can delete
        with self.login(self.gimli):
            response = self.post("pinax_comments:delete_comment", pk=comment.pk)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(Comment.objects.count(), 0)

    def test_ajax_delete_comment(self):
        d = Demo.objects.create(name="Wizard")
        with self.login(self.gimli):
            response = self.post_comment(d, data={
                "comment": "Wow, you're a jerk.",
            })
            comment = Comment.objects.get()

            response = self.post(
                "pinax_comments:delete_comment",
                pk=comment.pk,
                extra=dict(HTTP_X_REQUESTED_WITH="XMLHttpRequest")
            )
            self.assertEqual(response.status_code, 200)
            # Verify comment is deleted
            self.assertEqual(Comment.objects.count(), 0)

    def test_ajax_delete_comment_wrong_user(self):
        d = Demo.objects.create(name="Wizard")
        with self.login(self.gimli):
            response = self.post_comment(d, data={
                "comment": "Wow, you're a jerk.",
            })
            comment = Comment.objects.get()

        with self.login(self.aragorn):
            response = self.post(
                "pinax_comments:delete_comment",
                pk=comment.pk,
                extra=dict(HTTP_X_REQUESTED_WITH="XMLHttpRequest")
            )
            self.assertEqual(response.status_code, 200)
            # Verify comment is not deleted
            self.assertEqual(Comment.objects.count(), 1)

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
            c = Context({"o": d, "user": self.gimli})
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

    def test_ttag_can_edit_comment(self):
        d = Demo.objects.create(name="Wizard")
        with self.login(self.gimli):
            self.post_comment(d, data={
                "name": "Gandalf",
                "comment": "You can't win",
            })
            comment = Comment.objects.get()

        self.assert_renders(
            "{% load pinax_comments_tags %}{% if comment|can_edit_comment:user %}True{% else %}False{% endif %}",
            Context({"comment": comment, "user": self.gimli}),
            "True"
        )

        self.assert_renders(
            "{% load pinax_comments_tags %}{% if comment|can_edit_comment:user %}True{% else %}False{% endif %}",
            Context({"comment": comment, "user": self.aragorn}),
            "False"
        )

    def test_ttag_can_delete_comment(self):
        d = Demo.objects.create(name="Wizard")
        with self.login(self.gimli):
            self.post_comment(d, data={
                "name": "Gandalf",
                "comment": "You can't win",
            })
            comment = Comment.objects.get()

        self.assert_renders(
            "{% load pinax_comments_tags %}{% if comment|can_delete_comment:user %}True{% else %}False{% endif %}",
            Context({"comment": comment, "user": self.gimli}),
            "True"
        )

        self.assert_renders(
            "{% load pinax_comments_tags %}{% if comment|can_delete_comment:user %}True{% else %}False{% endif %}",
            Context({"comment": comment, "user": self.aragorn}),
            "False"
        )
