from __future__ import annotations

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User
from apps.users.services import sign_in_with_google


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
        read_only_fields = (
            "id",
            "email",
            "username",
            "followers_count",
            "following_count",
            "date_joined",
        )

    def get_followers_count(self, obj: User) -> int:
        return obj.follower_relationships.count()

    def get_following_count(self, obj: User) -> int:
        return obj.following_relationships.count()


class GoogleSignInSerializer(serializers.Serializer):
    id_token = serializers.CharField(required=False, write_only=True)
    credential = serializers.CharField(required=False, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    user = UserProfileSerializer(read_only=True)
    created = serializers.BooleanField(read_only=True)

    def validate(self, attrs: dict) -> dict:
        token = attrs.get("id_token") or attrs.get("credential")
        if not token:
            raise serializers.ValidationError("Either id_token or credential is required.")
        attrs["id_token"] = token
        return attrs

    def create(self, validated_data: dict) -> dict:
        result = sign_in_with_google(id_token_value=validated_data["id_token"])
        refresh = RefreshToken.for_user(result.user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": result.user,
            "created": result.created,
        }
