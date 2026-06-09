from __future__ import annotations

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from apps.comments.models import Comment
from apps.comments.services import create_comment, update_comment
from apps.posts.models import Post
from apps.users.serializers import UserPublicSerializer


def validation_detail(exc: DjangoValidationError):
    return getattr(exc, "message_dict", None) or exc.messages


class CommentSerializer(serializers.ModelSerializer):
    author = UserPublicSerializer(read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    post_id = serializers.PrimaryKeyRelatedField(
        source="post",
        queryset=Post.objects.all(),
        write_only=True,
        required=False,
    )

    class Meta:
        model = Comment
        fields = (
            "id",
            "post",
            "post_id",
            "author",
            "body",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "post", "author", "created_at", "updated_at")

    def validate(self, attrs: dict) -> dict:
        request = self.context.get("request")
        post = attrs.get("post")

        if self.instance is None and post is None:
            raise serializers.ValidationError({"post_id": "This field is required."})

        if post and (not request or not request.user.is_authenticated):
            raise serializers.ValidationError("Authentication is required to comment.")

        if post and not post.is_public and post.author != request.user:
            raise serializers.ValidationError("You cannot comment on this post.")

        return attrs

    def create(self, validated_data: dict) -> Comment:
        request = self.context["request"]
        try:
            return create_comment(author=request.user, **validated_data)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(validation_detail(exc)) from exc

    def update(self, instance: Comment, validated_data: dict) -> Comment:
        try:
            return update_comment(comment=instance, body=validated_data.get("body", instance.body))
        except DjangoValidationError as exc:
            raise serializers.ValidationError(validation_detail(exc)) from exc
