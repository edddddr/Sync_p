from __future__ import annotations

from django.contrib import admin

from apps.posts.models import Post, PostImage, PostLike


class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 0
    min_num = 1
    max_num = 4


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "place", "is_public", "created_at")
    list_filter = ("is_public", "created_at", "place__category")
    search_fields = ("caption", "author__username", "author__email", "place__name")
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("author", "place")
    inlines = (PostImageInline,)


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "order", "created_at")
    list_filter = ("created_at",)
    search_fields = ("post__caption", "post__author__username", "post__author__email")
    autocomplete_fields = ("post",)


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "post", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "user__email", "post__caption")
    autocomplete_fields = ("user", "post")
