from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import CreateView, DeleteView, UpdateView

from .forms import CommentForm
from .hooks import hookset
from .models import Comment
from .signals import comment_updated, commented

try:
    from account.mixins import LoginRequiredMixin
except ImportError:
    from django.contrib.auth.mixins import LoginRequiredMixin


class CommentSecureRedirectToMixin(object):

    def get_secure_redirect_to(self, object=None):
        redirect_to = self.request.POST.get("next")
        # light security check -- make sure redirect_to isn't garbage.
        if not redirect_to or " " in redirect_to or redirect_to.startswith("http"):
            try:
                if object is not None:
                    redirect_to = object.get_absolute_url()
                elif self.object is not None:
                    redirect_to = self.object.content_object.get_absolute_url()
            except AttributeError:
                raise ImproperlyConfigured(
                    "No URL to redirect to.  Either provide a url or define"
                    " a get_absolute_url method on the Model.")
        return redirect_to


class CommentCreateView(CommentSecureRedirectToMixin, CreateView):
    form_class = CommentForm
    content_object = None

    def get_form_kwargs(self):
        kwargs = super(CommentCreateView, self).get_form_kwargs()
        kwargs.update({
            "request": self.request,
            "obj": self.content_object,
            "user": self.request.user,
        })
        return kwargs

    def post(self, request, *args, **kwargs):
        content_type = get_object_or_404(ContentType, pk=self.kwargs.get("content_type_id"))
        self.content_object = content_type.get_object_for_this_type(pk=self.kwargs.get("object_id"))
        return super(CommentCreateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        commented.send(sender=self.content_object, comment=self.object, request=self.request)
        if self.request.is_ajax():
            data = {
                "status": "OK",
                "comment": self.object.data,
                "html": render_to_string("pinax/comments/_comment.html", {
                    "comment": self.object
                }, request=self.request)
            }
            return JsonResponse(data)
        return HttpResponseRedirect(self.get_secure_redirect_to(self.content_object))

    def form_invalid(self, form):
        if self.request.is_ajax():
            data = {
                "status": "ERROR",
                "errors": form.errors,
                "html": render_to_string("pinax/comments/_form.html", {
                    "form": form,
                    "obj": self.content_object
                }, request=self.request)
            }
            return JsonResponse(data)
        return HttpResponseRedirect(self.get_secure_redirect_to(self.content_object))


class CommentUpdateView(LoginRequiredMixin, CommentSecureRedirectToMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def get_form_kwargs(self):
        kwargs = super(CommentUpdateView, self).get_form_kwargs()
        kwargs.update({
            "request": self.request,
            "obj": self.object.content_object,
            "user": self.request.user,
        })
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        comment_updated.send(sender=self.object.content_object, comment=self.object, request=self.request)
        if self.request.is_ajax():
            data = {
                "status": "OK",
                "comment": self.object.data
            }
            return JsonResponse(data)
        return HttpResponseRedirect(self.get_secure_redirect_to())

    def form_invalid(self, form):
        if self.request.is_ajax():
            data = {
                "status": "ERROR",
                "errors": form.errors
            }
            return JsonResponse(data)
        return HttpResponseRedirect(self.get_secure_redirect_to())


class CommentDeleteView(LoginRequiredMixin, CommentSecureRedirectToMixin, DeleteView):
    model = Comment

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_secure_redirect_to()
        if hookset.load_can_delete(request.user, self.object):
            self.object.delete()
            if request.is_ajax():
                return JsonResponse({"status": "OK"})
        else:
            if request.is_ajax():
                return JsonResponse({"status": "ERROR", "errors": "You do not have permission to delete this comment."})
        return HttpResponseRedirect(success_url)
