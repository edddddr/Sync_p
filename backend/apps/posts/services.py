from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.notifications.services import notify_post_like
from apps.places.models import Place
from apps.posts.models import Post, PostImage, PostLike
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


def validate_post_images(images: list | None, *, required: bool) -> list:
    if not images:
        if required:
            raise ValidationError("Posts must include at least 1 image.")
        return []

    if len(images) > 4:
        raise ValidationError("Posts can have at most 4 images.")

    return images


@transaction.atomic
def create_post(*, author: User, place: Place, images: list, **post_data) -> Post:
    images = validate_post_images(images, required=True)
    post_data["tags"] = normalize_tags(post_data.get("tags"))
    if post_data.get("latitude") is None:
        post_data["latitude"] = place.latitude
    if post_data.get("longitude") is None:
        post_data["longitude"] = place.longitude

    post = Post(author=author, place=place, **post_data)
    post.full_clean()
    post.save()
    create_post_images(post=post, images=images)
    return post


@transaction.atomic
def update_post(*, post: Post, images: list | None = None, **post_data) -> Post:
    if "tags" in post_data:
        post_data["tags"] = normalize_tags(post_data.get("tags"))

    for field, value in post_data.items():
        setattr(post, field, value)

    post.full_clean()
    post.save()

    if images is not None:
        images = validate_post_images(images, required=True)
        post.images.all().delete()
        create_post_images(post=post, images=images)

    return post


def create_post_images(*, post: Post, images: list) -> None:
    PostImage.objects.bulk_create(
        [
            PostImage(post=post, image=image, order=index)
            for index, image in enumerate(images)
        ]
    )


def like_post(*, user: User, post: Post) -> tuple[PostLike, bool]:
    like, created = PostLike.objects.get_or_create(user=user, post=post)
    if created:
        notify_post_like(actor=user, post=post)
    return like, created


def unlike_post(*, user: User, post: Post) -> int:
    deleted_count, _ = PostLike.objects.filter(user=user, post=post).delete()
    return deleted_count
