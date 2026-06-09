# Generated for the initial SyncP post domain.
from __future__ import annotations

import decimal

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
            name="Post",
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
                ("image", models.ImageField(upload_to="posts/%Y/%m/")),
                ("caption", models.TextField(blank=True)),
                ("tags", models.JSONField(blank=True, default=list)),
                (
                    "latitude",
                    models.DecimalField(
                        blank=True,
                        decimal_places=6,
                        max_digits=9,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(decimal.Decimal("-90.0")),
                            django.core.validators.MaxValueValidator(decimal.Decimal("90.0")),
                        ],
                    ),
                ),
                (
                    "longitude",
                    models.DecimalField(
                        blank=True,
                        decimal_places=6,
                        max_digits=9,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(decimal.Decimal("-180.0")),
                            django.core.validators.MaxValueValidator(decimal.Decimal("180.0")),
                        ],
                    ),
                ),
                ("is_public", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="posts",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "place",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="posts",
                        to="places.place",
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at",),
                "indexes": [
                    models.Index(fields=["-created_at"], name="posts_created_idx"),
                    models.Index(fields=["author", "-created_at"], name="posts_author_created_idx"),
                    models.Index(fields=["place", "-created_at"], name="posts_place_created_idx"),
                    models.Index(
                        fields=["is_public", "-created_at"],
                        name="posts_public_created_idx",
                    ),
                ],
                "constraints": [
                    models.CheckConstraint(
                        condition=(
                            models.Q(("latitude__isnull", True))
                            | (models.Q(("latitude__gte", -90)) & models.Q(("latitude__lte", 90)))
                        ),
                        name="post_latitude_range",
                    ),
                    models.CheckConstraint(
                        condition=(
                            models.Q(("longitude__isnull", True))
                            | (
                                models.Q(("longitude__gte", -180))
                                & models.Q(("longitude__lte", 180))
                            )
                        ),
                        name="post_longitude_range",
                    ),
                ],
            },
        ),
    ]
