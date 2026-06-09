from __future__ import annotations

from django.utils import timezone

from apps.notifications.models import Notification, NotificationType
from apps.users.models import User


def create_notification(
    *,
    recipient: User | None,
    actor: User,
    notification_type: str,
    message: str,
    target_url: str = "",
    data: dict | None = None,
) -> Notification | None:
    if recipient is None or recipient.pk == actor.pk:
        return None

    return Notification.objects.create(
        recipient=recipient,
        actor=actor,
        notification_type=notification_type,
        message=message,
        target_url=target_url,
        data=data or {},
    )


def notify_follow(*, follower: User, following: User) -> Notification | None:
    return create_notification(
        recipient=following,
        actor=follower,
        notification_type=NotificationType.FOLLOW,
        message=f"{follower} started following you.",
        target_url=f"/users/{follower.id}",
        data={"user_id": follower.id},
    )


def notify_post_like(*, actor: User, post) -> Notification | None:
    return create_notification(
        recipient=post.author,
        actor=actor,
        notification_type=NotificationType.LIKE,
        message=f"{actor} liked your post.",
        target_url=f"/posts/{post.id}",
        data={"post_id": post.id},
    )


def notify_post_comment(*, actor: User, comment) -> Notification | None:
    return create_notification(
        recipient=comment.post.author,
        actor=actor,
        notification_type=NotificationType.COMMENT,
        message=f"{actor} commented on your post.",
        target_url=f"/posts/{comment.post_id}",
        data={"post_id": comment.post_id, "comment_id": comment.id},
    )


def notify_post_bookmark(*, actor: User, post) -> Notification | None:
    return create_notification(
        recipient=post.author,
        actor=actor,
        notification_type=NotificationType.BOOKMARK,
        message=f"{actor} bookmarked your post.",
        target_url=f"/posts/{post.id}",
        data={"post_id": post.id},
    )


def notify_place_rating(*, actor: User, rating) -> Notification | None:
    return create_notification(
        recipient=rating.place.created_by,
        actor=actor,
        notification_type=NotificationType.RATING,
        message=f"{actor} rated your place {rating.score}/5.",
        target_url=f"/places/{rating.place.slug}",
        data={"place_id": rating.place_id, "rating_id": rating.id, "score": rating.score},
    )


def mark_notification_read(*, notification: Notification) -> Notification:
    if not notification.is_read:
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save(update_fields=["is_read", "read_at"])
    return notification


def mark_notification_unread(*, notification: Notification) -> Notification:
    if notification.is_read:
        notification.is_read = False
        notification.read_at = None
        notification.save(update_fields=["is_read", "read_at"])
    return notification


def mark_all_notifications_read(*, recipient: User) -> int:
    return Notification.objects.filter(recipient=recipient, is_read=False).update(
        is_read=True,
        read_at=timezone.now(),
    )
