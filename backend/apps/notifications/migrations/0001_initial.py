# Generated for the initial SyncP notification domain.
from __future__ import annotations

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Notification",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "notification_type",
                    models.CharField(
                        choices=[
                            ("follow", "Follow"),
                            ("like", "Like"),
                            ("comment", "Comment"),
                            ("bookmark", "Bookmark"),
                            ("rating", "Rating"),
                        ],
                        max_length=32,
                    ),
                ),
                ("message", models.CharField(max_length=255)),
                ("target_url", models.CharField(blank=True, max_length=255)),
                ("data", models.JSONField(blank=True, default=dict)),
                ("is_read", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("read_at", models.DateTimeField(blank=True, null=True)),
                (
                    "actor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notifications_sent",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "recipient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notifications",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at",),
                "indexes": [
                    models.Index(
                        fields=["recipient", "is_read", "-created_at"],
                        name="notif_recipient_read_idx",
                    ),
                    models.Index(
                        fields=["recipient", "-created_at"],
                        name="notif_recipient_created_idx",
                    ),
                    models.Index(fields=["notification_type"], name="notif_type_idx"),
                ],
            },
        ),
    ]

