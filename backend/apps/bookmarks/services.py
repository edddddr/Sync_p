from __future__ import annotations

from apps.bookmarks.models import Bookmark
from apps.notifications.services import notify_post_bookmark
from apps.posts.models import Post
from apps.users.models import User


def bookmark_post(*, user: User, post: Post) -> tuple[Bookmark, bool]:
    bookmark, created = Bookmark.objects.get_or_create(user=user, post=post)
    if created:
        notify_post_bookmark(actor=user, post=post)
    return bookmark, created


def unbookmark_post(*, user: User, post: Post) -> int:
    deleted_count, _ = Bookmark.objects.filter(user=user, post=post).delete()
    return deleted_count
