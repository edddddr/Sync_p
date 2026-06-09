from __future__ import annotations

from decimal import Decimal

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify


def build_unique_place_slug(place: "Place") -> str:
    base = slugify(f"{place.name}-{place.city}") or slugify(place.name) or "place"
    base = base[:80]
    slug = base
    counter = 2

    while Place.objects.filter(slug=slug).exclude(pk=place.pk).exists():
        suffix = f"-{counter}"
        slug = f"{base[:96 - len(suffix)]}{suffix}"
        counter += 1

    return slug


class PlaceCategory(models.TextChoices):
    CAFE = "cafe", "Cafe"
    PARK = "park", "Park"
    MOUNTAIN = "mountain", "Mountain"
    WORKSPACE = "workspace", "Workspace"
    GAMING = "gaming", "Gaming place"
    HIDDEN_SPOT = "hidden_spot", "Hidden spot"
    TOURIST = "tourist", "Tourist place"
    RESTAURANT = "restaurant", "Restaurant"
    OTHER = "other", "Other"


class Place(models.Model):
    name = models.CharField(max_length=160)
    slug = models.SlugField(max_length=96, unique=True, blank=True)
    category = models.CharField(
        max_length=32,
        choices=PlaceCategory.choices,
        default=PlaceCategory.OTHER,
    )
    description = models.TextField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=120, blank=True)
    country = models.CharField(max_length=120, blank=True)
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[
            MinValueValidator(Decimal("-90.0")),
            MaxValueValidator(Decimal("90.0")),
        ],
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[
            MinValueValidator(Decimal("-180.0")),
            MaxValueValidator(Decimal("180.0")),
        ],
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="places",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)
        indexes = [
            models.Index(fields=["category"], name="places_category_idx"),
            models.Index(fields=["city", "country"], name="places_city_country_idx"),
            models.Index(fields=["-created_at"], name="places_created_idx"),
            models.Index(fields=["latitude", "longitude"], name="places_location_idx"),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(latitude__gte=-90) & models.Q(latitude__lte=90),
                name="place_latitude_range",
            ),
            models.CheckConstraint(
                condition=models.Q(longitude__gte=-180) & models.Q(longitude__lte=180),
                name="place_longitude_range",
            ),
        ]

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = build_unique_place_slug(self)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        location = ", ".join(part for part in (self.city, self.country) if part)
        return f"{self.name} ({location})" if location else self.name
