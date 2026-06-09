from __future__ import annotations

from django.contrib import admin

from apps.bookmarks.models import Bookmark


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "post", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "user__email", "post__caption")
    autocomplete_fields = ("user", "post")
