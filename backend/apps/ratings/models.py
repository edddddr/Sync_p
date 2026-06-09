from __future__ import annotations

from django.conf import settings
from django.core.validators import MaxLengthValidator, MaxValueValidator, MinValueValidator
from django.db import models

from apps.places.models import Place


class PlaceRating(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="place_ratings",
    )
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name="ratings",
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
    )
    review = models.TextField(blank=True, validators=[MaxLengthValidator(1000)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-updated_at",)
        indexes = [
            models.Index(fields=["place", "-updated_at"], name="ratings_place_updated_idx"),
            models.Index(fields=["user", "-updated_at"], name="ratings_user_updated_idx"),
            models.Index(fields=["score"], name="ratings_score_idx"),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=("user", "place"),
                name="unique_place_rating",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.user} rated {self.place} {self.score}/5"
