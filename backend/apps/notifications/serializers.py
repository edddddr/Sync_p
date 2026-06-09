from __future__ import annotations

from rest_framework import serializers

from apps.notifications.models import Notification
from apps.users.serializers import UserPublicSerializer


class NotificationSerializer(serializers.ModelSerializer):
    actor = UserPublicSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = (
            "id",
            "actor",
            "notification_type",
            "message",
            "target_url",
            "data",
            "is_read",
            "created_at",
            "read_at",
        )
        read_only_fields = fields
