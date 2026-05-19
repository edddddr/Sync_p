from __future__ import annotations

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.users.models import User


class UserPublicSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "display_name",
            "bio",
            "avatar",
            "location",
            "website",
            "followers_count",
            "following_count",
            "date_joined",
        )
        read_only_fields = fields

    def get_followers_count(self, obj: User) -> int:
        return obj.follower_relationships.count()

    def get_following_count(self, obj: User) -> int:
        return obj.following_relationships.count()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    class Meta:
        model = User
        fields = ("id", "email", "username", "password", "display_name")
        read_only_fields = ("id",)

    def validate_email(self, value: str) -> str:
        return value.lower()

    def validate_password(self, value: str) -> str:
        validate_password(value)
        return value

    def create(self, validated_data: dict) -> User:
        return User.objects.create_user(**validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "display_name",
            "bio",
            "avatar",
            "location",
            "website",
            "followers_count",
            "following_count",
            "date_joined",
        )
        read_only_fields = ("id", "email", "username", "followers_count", "following_count", "date_joined")

    def get_followers_count(self, obj: User) -> int:
        return obj.follower_relationships.count()

    def get_following_count(self, obj: User) -> int:
        return obj.following_relationships.count()

