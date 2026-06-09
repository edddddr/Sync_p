from __future__ import annotations

from apps.places.models import Place
from apps.users.models import User


def create_place(*, created_by: User | None, **place_data) -> Place:
    place = Place(created_by=created_by, **place_data)
    place.full_clean()
    place.save()
    return place


def update_place(*, place: Place, **place_data) -> Place:
    for field, value in place_data.items():
        setattr(place, field, value)

    place.full_clean()
    place.save()
    return place
