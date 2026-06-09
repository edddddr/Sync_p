from __future__ import annotations

from django.conf import settings
from django.db import models

from apps.posts.models import Post


class Bookmark(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookmarks",
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="bookmarks",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["user", "-created_at"], name="bookmarks_user_created_idx"),
            models.Index(fields=["post", "-created_at"], name="bookmarks_post_created_idx"),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=("user", "post"),
                name="unique_post_bookmark",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.user} bookmarked post {self.post_id}"
