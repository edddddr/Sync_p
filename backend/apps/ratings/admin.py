from __future__ import annotations

from django.contrib import admin

from apps.ratings.models import PlaceRating


@admin.register(PlaceRating)
class PlaceRatingAdmin(admin.ModelAdmin):
    list_display = ("id", "place", "user", "score", "created_at", "updated_at")
    list_filter = ("score", "created_at", "updated_at")
    search_fields = ("place__name", "user__username", "user__email", "review")
    autocomplete_fields = ("place", "user")
