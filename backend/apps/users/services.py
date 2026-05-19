from __future__ import annotations

from django.core.exceptions import ValidationError

from apps.users.models import Follow, User


def follow_user(*, follower: User, following: User) -> tuple[Follow, bool]:
    if follower.pk == following.pk:
        raise ValidationError("Users cannot follow themselves.")

    return Follow.objects.get_or_create(follower=follower, following=following)


def unfollow_user(*, follower: User, following: User) -> int:
    deleted_count, _ = Follow.objects.filter(follower=follower, following=following).delete()
    return deleted_count

