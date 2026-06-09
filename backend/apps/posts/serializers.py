from __future__ import annotations

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from apps.places.models import Place
from apps.places.serializers import PlaceSerializer
from apps.posts.models import Post
from apps.posts.services import create_post, normalize_tags, update_post
from apps.users.serializers import UserPublicSerializer


def validation_detail(exc: DjangoValidationError):
    return getattr(exc, "message_dict", None) or exc.messages


class PostReadSerializer(serializers.ModelSerializer):
    author = UserPublicSerializer(read_only=True)
    place = PlaceSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    bookmarks_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "place",
            "image",
            "caption",
            "tags",
            "latitude",
            "longitude",
            "is_public",
            "likes_count",
            "comments_count",
            "bookmarks_count",
            "is_liked",
            "is_bookmarked",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields

    def get_likes_count(self, obj: Post) -> int:
        return obj.likes.count()

    def get_comments_count(self, obj: Post) -> int:
        return obj.comments.count()

    def get_bookmarks_count(self, obj: Post) -> int:
        return obj.bookmarks.count()

    def get_is_liked(self, obj: Post) -> bool:
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return obj.likes.filter(user=request.user).exists()

    def get_is_bookmarked(self, obj: Post) -> bool:
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return obj.bookmarks.filter(user=request.user).exists()


class PostWriteSerializer(serializers.ModelSerializer):
    place_id = serializers.PrimaryKeyRelatedField(
        source="place",
        queryset=Place.objects.all(),
        write_only=True,
    )
    tags = serializers.ListField(
        child=serializers.CharField(max_length=40),
        required=False,
        allow_empty=True,
    )

    class Meta:
        model = Post
        fields = (
            "id",
            "place_id",
            "image",
            "caption",
            "tags",
            "latitude",
            "longitude",
            "is_public",
        )
        read_only_fields = ("id",)

    def validate_tags(self, value: list[str]) -> list[str]:
        try:
            return normalize_tags(value)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(exc.messages) from exc

    def validate(self, attrs: dict) -> dict:
        request = self.context.get("request")
        place = attrs.get("place")

        if place and (not request or not request.user.is_authenticated):
            raise serializers.ValidationError("Authentication is required to create posts.")

        return attrs

    def create(self, validated_data: dict) -> Post:
        request = self.context["request"]
        try:
            return create_post(author=request.user, **validated_data)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(validation_detail(exc)) from exc

    def update(self, instance: Post, validated_data: dict) -> Post:
        try:
            return update_post(post=instance, **validated_data)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(validation_detail(exc)) from exc

    def to_representation(self, instance: Post) -> dict:
        return PostReadSerializer(instance, context=self.context).data
