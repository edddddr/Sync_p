from __future__ import annotations

from django.contrib import admin

from apps.posts.models import Post, PostLike


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "place", "is_public", "created_at")
    list_filter = ("is_public", "created_at", "place__category")
    search_fields = ("caption", "author__username", "author__email", "place__name")
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("author", "place")


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "post", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "user__email", "post__caption")
    autocomplete_fields = ("user", "post")
