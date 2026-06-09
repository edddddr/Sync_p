from __future__ import annotations

from django.contrib import admin

from apps.places.models import Place


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "city", "country", "created_by", "created_at")
    list_filter = ("category", "country", "created_at")
    search_fields = ("name", "address", "city", "country")
    readonly_fields = ("slug", "created_at", "updated_at")
    autocomplete_fields = ("created_by",)
