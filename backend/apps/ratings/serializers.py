from __future__ import annotations

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from apps.places.models import Place
from apps.places.serializers import PlaceSerializer
from apps.ratings.models import PlaceRating
from apps.ratings.services import rate_place, update_rating
from apps.users.serializers import UserPublicSerializer


def validation_detail(exc: DjangoValidationError):
    return getattr(exc, "message_dict", None) or exc.messages


class PlaceRatingSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)
    place = PlaceSerializer(read_only=True)
    place_id = serializers.PrimaryKeyRelatedField(
        source="place",
        queryset=Place.objects.all(),
        write_only=True,
        required=False,
    )

    class Meta:
        model = PlaceRating
        fields = (
            "id",
            "user",
            "place",
            "place_id",
            "score",
            "review",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "user", "place", "created_at", "updated_at")

    def validate(self, attrs: dict) -> dict:
        if self.instance is None and attrs.get("place") is None:
            raise serializers.ValidationError({"place_id": "This field is required."})
        return attrs

    def create(self, validated_data: dict) -> PlaceRating:
        request = self.context["request"]
        try:
            rating, _created = rate_place(user=request.user, **validated_data)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(validation_detail(exc)) from exc
        return rating

    def update(self, instance: PlaceRating, validated_data: dict) -> PlaceRating:
        validated_data.pop("place", None)
        try:
            return update_rating(rating=instance, **validated_data)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(validation_detail(exc)) from exc
