from __future__ import annotations

from decimal import Decimal

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.places.models import Place


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
    )
    place = models.ForeignKey(
        Place,
        on_delete=models.PROTECT,
        related_name="posts",
    )
    caption = models.TextField(blank=True)
    tags = models.JSONField(default=list, blank=True)
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        validators=[
            MinValueValidator(Decimal("-90.0")),
            MaxValueValidator(Decimal("90.0")),
        ],
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        validators=[
            MinValueValidator(Decimal("-180.0")),
            MaxValueValidator(Decimal("180.0")),
        ],
    )
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["-created_at"], name="posts_created_idx"),
            models.Index(fields=["author", "-created_at"], name="posts_author_created_idx"),
            models.Index(fields=["place", "-created_at"], name="posts_place_created_idx"),
            models.Index(fields=["is_public", "-created_at"], name="posts_public_created_idx"),
        ]
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(latitude__isnull=True)
                    | (models.Q(latitude__gte=-90) & models.Q(latitude__lte=90))
                ),
                name="post_latitude_range",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(longitude__isnull=True)
                    | (models.Q(longitude__gte=-180) & models.Q(longitude__lte=180))
                ),
                name="post_longitude_range",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.author} at {self.place}"


class PostImage(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(upload_to="posts/%Y/%m/")
    order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("order", "id")
        indexes = [
            models.Index(fields=["post", "order"], name="posts_image_post_order_idx"),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=("post", "order"),
                name="unique_post_image_order",
            ),
            models.CheckConstraint(
                condition=models.Q(order__gte=0) & models.Q(order__lte=3),
                name="post_image_order_range",
            ),
        ]

    def __str__(self) -> str:
        return f"image {self.order} for post {self.post_id}"


class PostLike(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="post_likes",
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["user", "post"], name="posts_like_user_post_idx"),
            models.Index(fields=["post", "-created_at"], name="posts_like_post_created_idx"),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=("user", "post"),
                name="unique_post_like",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.user} liked post {self.post_id}"
