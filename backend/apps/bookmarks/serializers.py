from __future__ import annotations

from rest_framework import serializers

from apps.bookmarks.models import Bookmark
from apps.bookmarks.services import bookmark_post
from apps.posts.models import Post
from apps.posts.serializers import PostReadSerializer


class BookmarkSerializer(serializers.ModelSerializer):
    post = PostReadSerializer(read_only=True)
    post_id = serializers.PrimaryKeyRelatedField(
        source="post",
        queryset=Post.objects.all(),
        write_only=True,
    )

    class Meta:
        model = Bookmark
        fields = (
            "id",
            "post",
            "post_id",
            "created_at",
        )
        read_only_fields = ("id", "post", "created_at")

    def validate(self, attrs: dict) -> dict:
        request = self.context.get("request")
        post = attrs.get("post")

        if post and (not request or not request.user.is_authenticated):
            raise serializers.ValidationError("Authentication is required to bookmark posts.")

        if post and not post.is_public and post.author != request.user:
            raise serializers.ValidationError("You cannot bookmark this post.")

        return attrs

    def create(self, validated_data: dict) -> Bookmark:
        request = self.context["request"]
        bookmark, _created = bookmark_post(user=request.user, **validated_data)
        return bookmark
