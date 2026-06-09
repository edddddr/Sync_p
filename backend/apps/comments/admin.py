from __future__ import annotations

from django.contrib import admin

from apps.comments.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "author", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("body", "author__username", "author__email", "post__caption")
    autocomplete_fields = ("post", "author")
