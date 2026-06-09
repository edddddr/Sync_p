from __future__ import annotations

from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import models
from rest_framework import serializers

from apps.places.models import Place
from apps.places.services import create_place, update_place
from apps.users.serializers import UserPublicSerializer


def validation_detail(exc: DjangoValidationError):
    return getattr(exc, "message_dict", None) or exc.messages


class PlaceSerializer(serializers.ModelSerializer):
    created_by = UserPublicSerializer(read_only=True)
    posts_count = serializers.SerializerMethodField()
    ratings_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Place
        fields = (
            "id",
            "name",
            "slug",
            "category",
            "description",
            "address",
            "city",
            "country",
            "latitude",
            "longitude",
            "created_by",
            "posts_count",
            "ratings_count",
            "average_rating",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "slug",
            "created_by",
            "posts_count",
            "ratings_count",
            "average_rating",
            "created_at",
            "updated_at",
        )

    def get_posts_count(self, obj: Place) -> int:
        annotated_count = getattr(obj, "posts_count", None)
        if annotated_count is not None:
            return annotated_count
        return obj.posts.filter(is_public=True).count()

    def get_ratings_count(self, obj: Place) -> int:
        annotated_count = getattr(obj, "ratings_count", None)
        if annotated_count is not None:
            return annotated_count
        return obj.ratings.count()

    def get_average_rating(self, obj: Place) -> float | None:
        annotated_average = getattr(obj, "average_rating", None)
        if annotated_average is None:
            annotated_average = obj.ratings.aggregate(
                average=models.Avg("score"),
            )["average"]

        if annotated_average is None:
            return None
        return round(float(annotated_average), 2)

    def create(self, validated_data: dict) -> Place:
        request = self.context.get("request")
        created_by = request.user if request and request.user.is_authenticated else None
        try:
            return create_place(created_by=created_by, **validated_data)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(validation_detail(exc)) from exc

    def update(self, instance: Place, validated_data: dict) -> Place:
        try:
            return update_place(place=instance, **validated_data)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(validation_detail(exc)) from exc
