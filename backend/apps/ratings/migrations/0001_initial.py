# Generated for the initial SyncP rating domain.
from __future__ import annotations

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("places", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="PlaceRating",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "score",
                    models.PositiveSmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(5),
                        ],
                    ),
                ),
                (
                    "review",
                    models.TextField(
                        blank=True,
                        validators=[django.core.validators.MaxLengthValidator(1000)],
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "place",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ratings",
                        to="places.place",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="place_ratings",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("-updated_at",),
                "indexes": [
                    models.Index(fields=["place", "-updated_at"], name="ratings_place_updated_idx"),
                    models.Index(fields=["user", "-updated_at"], name="ratings_user_updated_idx"),
                    models.Index(fields=["score"], name="ratings_score_idx"),
                ],
                "constraints": [
                    models.UniqueConstraint(
                        fields=("user", "place"),
                        name="unique_place_rating",
                    ),
                ],
            },
        ),
    ]

