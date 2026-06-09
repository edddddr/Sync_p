from __future__ import annotations

from django.conf import settings
from django.db import models


class NotificationType(models.TextChoices):
    FOLLOW = "follow", "Follow"
    LIKE = "like", "Like"
    COMMENT = "comment", "Comment"
    BOOKMARK = "bookmark", "Bookmark"
    RATING = "rating", "Rating"


class Notification(models.Model):
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications_sent",
    )
    notification_type = models.CharField(max_length=32, choices=NotificationType.choices)
    message = models.CharField(max_length=255)
    target_url = models.CharField(max_length=255, blank=True)
    data = models.JSONField(default=dict, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(
                fields=["recipient", "is_read", "-created_at"],
                name="notif_recipient_read_idx",
            ),
            models.Index(fields=["recipient", "-created_at"], name="notif_recipient_created_idx"),
            models.Index(fields=["notification_type"], name="notif_type_idx"),
        ]

    def __str__(self) -> str:
        return f"{self.notification_type} for {self.recipient}"
