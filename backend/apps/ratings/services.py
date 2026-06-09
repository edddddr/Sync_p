from __future__ import annotations

from apps.places.models import Place
from apps.ratings.models import PlaceRating
from apps.users.models import User


def rate_place(
    *,
    user: User,
    place: Place,
    score: int,
    review: str = "",
) -> tuple[PlaceRating, bool]:
    rating, created = PlaceRating.objects.update_or_create(
        user=user,
        place=place,
        defaults={
            "score": score,
            "review": review,
        },
    )
    return rating, created


def update_rating(*, rating: PlaceRating, score: int | None = None, review: str | None = None):
    if score is not None:
        rating.score = score
    if review is not None:
        rating.review = review

    rating.full_clean()
    rating.save()
    return rating
