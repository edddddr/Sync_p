from __future__ import annotations

from django.core.exceptions import ValidationError

from apps.notifications.services import notify_post_like
from apps.places.models import Place
from apps.posts.models import Post, PostLike
from apps.users.models import User


def normalize_tags(tags: list[str] | None) -> list[str]:
    if not tags:
        return []

    normalized: list[str] = []
    seen: set[str] = set()

    for raw_tag in tags:
        tag = raw_tag.strip().lower().lstrip("#")
        if not tag or tag in seen:
            continue
        if len(tag) > 40:
            raise ValidationError("Tags must be 40 characters or fewer.")
        normalized.append(tag)
        seen.add(tag)

    if len(normalized) > 10:
        raise ValidationError("Posts can have at most 10 tags.")

    return normalized


def create_post(*, author: User, place: Place, **post_data) -> Post:
    post_data["tags"] = normalize_tags(post_data.get("tags"))
    if post_data.get("latitude") is None:
        post_data["latitude"] = place.latitude
    if post_data.get("longitude") is None:
        post_data["longitude"] = place.longitude

    post = Post(author=author, place=place, **post_data)
    post.full_clean()
    post.save()
    return post


def update_post(*, post: Post, **post_data) -> Post:
    if "tags" in post_data:
        post_data["tags"] = normalize_tags(post_data.get("tags"))

    for field, value in post_data.items():
        setattr(post, field, value)

    post.full_clean()
    post.save()
    return post


def like_post(*, user: User, post: Post) -> tuple[PostLike, bool]:
    like, created = PostLike.objects.get_or_create(user=user, post=post)
    if created:
        notify_post_like(actor=user, post=post)
    return like, created


def unlike_post(*, user: User, post: Post) -> int:
    deleted_count, _ = PostLike.objects.filter(user=user, post=post).delete()
    return deleted_count
