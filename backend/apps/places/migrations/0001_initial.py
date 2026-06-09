# Generated for the initial SyncP place domain.
from __future__ import annotations

import decimal

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Place",
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
                ("name", models.CharField(max_length=160)),
                ("slug", models.SlugField(blank=True, max_length=96, unique=True)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("cafe", "Cafe"),
                            ("park", "Park"),
                            ("mountain", "Mountain"),
                            ("workspace", "Workspace"),
                            ("gaming", "Gaming place"),
                            ("hidden_spot", "Hidden spot"),
                            ("tourist", "Tourist place"),
                            ("restaurant", "Restaurant"),
                            ("other", "Other"),
                        ],
                        default="other",
                        max_length=32,
                    ),
                ),
                ("description", models.TextField(blank=True)),
                ("address", models.CharField(blank=True, max_length=255)),
                ("city", models.CharField(blank=True, max_length=120)),
                ("country", models.CharField(blank=True, max_length=120)),
                (
                    "latitude",
                    models.DecimalField(
                        decimal_places=6,
                        max_digits=9,
                        validators=[
                            django.core.validators.MinValueValidator(decimal.Decimal("-90.0")),
                            django.core.validators.MaxValueValidator(decimal.Decimal("90.0")),
                        ],
                    ),
                ),
                (
                    "longitude",
                    models.DecimalField(
                        decimal_places=6,
                        max_digits=9,
                        validators=[
                            django.core.validators.MinValueValidator(decimal.Decimal("-180.0")),
                            django.core.validators.MaxValueValidator(decimal.Decimal("180.0")),
                        ],
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="places",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("name",),
                "indexes": [
                    models.Index(fields=["category"], name="places_category_idx"),
                    models.Index(fields=["city", "country"], name="places_city_country_idx"),
                    models.Index(fields=["-created_at"], name="places_created_idx"),
                    models.Index(fields=["latitude", "longitude"], name="places_location_idx"),
                ],
                "constraints": [
                    models.CheckConstraint(
                        condition=models.Q(("latitude__gte", -90), ("latitude__lte", 90)),
                        name="place_latitude_range",
                    ),
                    models.CheckConstraint(
                        condition=models.Q(("longitude__gte", -180), ("longitude__lte", 180)),
                        name="place_longitude_range",
                    ),
                ],
            },
        ),
    ]

