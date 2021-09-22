from django.contrib import admin

from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ["author", "content_type", "public"]
    list_filter = ["public", "content_type"]
    autocomplete_fields = ['author']


admin.site.register(Comment, CommentAdmin)
