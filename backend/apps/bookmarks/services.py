from __future__ import annotations

from apps.bookmarks.models import Bookmark
from apps.posts.models import Post
from apps.users.models import User


def bookmark_post(*, user: User, post: Post) -> tuple[Bookmark, bool]:
    return Bookmark.objects.get_or_create(user=user, post=post)


def unbookmark_post(*, user: User, post: Post) -> int:
    deleted_count, _ = Bookmark.objects.filter(user=user, post=post).delete()
    return deleted_count
