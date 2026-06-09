from __future__ import annotations

from django.conf import settings
from django.core.validators import MaxLengthValidator
from django.db import models

from apps.posts.models import Post


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    body = models.TextField(validators=[MaxLengthValidator(1000)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("created_at",)
        indexes = [
            models.Index(fields=["post", "created_at"], name="comments_post_created_idx"),
            models.Index(fields=["author", "-created_at"], name="comments_author_created_idx"),
        ]

    def __str__(self) -> str:
        return f"{self.author} on post {self.post_id}"
