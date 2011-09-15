from django.contrib import admin

from dialogos.models import Comment


class CommentAdmin(admin.ModelAdmin):  
    list_display = ["author", "content_type", "public"]
    list_filter = ["public", "content_type"]


admin.site.register(Comment, CommentAdmin)
