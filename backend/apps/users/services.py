from __future__ import annotations

from dataclasses import dataclass

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.text import slugify

from apps.notifications.services import notify_follow
from apps.users.models import Follow, SocialAccount, SocialProvider, User


def follow_user(*, follower: User, following: User) -> tuple[Follow, bool]:
    if follower.pk == following.pk:
        raise ValidationError("Users cannot follow themselves.")

    follow, created = Follow.objects.get_or_create(follower=follower, following=following)
    if created:
        notify_follow(follower=follower, following=following)
    return follow, created


def unfollow_user(*, follower: User, following: User) -> int:
    deleted_count, _ = Follow.objects.filter(follower=follower, following=following).delete()
    return deleted_count


@dataclass(frozen=True)
class GoogleAuthResult:
    user: User
    social_account: SocialAccount
    created: bool


def build_unique_username(*, email: str, fallback: str) -> str:
    base = slugify(email.split("@")[0]) or slugify(fallback) or "user"
    base = base[:120]
    username = base
    counter = 2

    while User.objects.filter(username=username).exists():
        suffix = f"-{counter}"
        username = f"{base[:150 - len(suffix)]}{suffix}"
        counter += 1

    return username


def verify_google_id_token(*, id_token_value: str) -> dict:
    client_ids = [client_id for client_id in settings.GOOGLE_OAUTH_CLIENT_IDS if client_id]
    if not client_ids:
        raise ValidationError("Google OAuth is not configured.")

    try:
        from google.auth.transport import requests
        from google.oauth2 import id_token
    except ImportError as exc:
        raise ValidationError("Google OAuth dependencies are not installed.") from exc

    try:
        payload = id_token.verify_oauth2_token(id_token_value, requests.Request())
    except ValueError as exc:
        raise ValidationError("Invalid Google ID token.") from exc

    if payload.get("aud") not in client_ids:
        raise ValidationError("Google ID token audience is not allowed.")
    if not payload.get("email"):
        raise ValidationError("Google account did not provide an email address.")
    if payload.get("email_verified") is not True:
        raise ValidationError("Google email address is not verified.")

    return payload


@transaction.atomic
def sign_in_with_google(*, id_token_value: str) -> GoogleAuthResult:
    payload = verify_google_id_token(id_token_value=id_token_value)
    provider_user_id = payload["sub"]
    email = User.objects.normalize_email(payload["email"]).lower()
    display_name = payload.get("name") or email.split("@")[0]

    social_account = (
        SocialAccount.objects.select_related("user")
        .filter(provider=SocialProvider.GOOGLE, provider_user_id=provider_user_id)
        .first()
    )
    if social_account is not None:
        return GoogleAuthResult(
            user=social_account.user,
            social_account=social_account,
            created=False,
        )

    user = User.objects.filter(email=email).first()
    created = False

    if user is None:
        user = User.objects.create_user(
            email=email,
            username=build_unique_username(email=email, fallback=provider_user_id),
            password=None,
            display_name=display_name,
        )
        created = True
    elif not user.display_name:
        user.display_name = display_name
        user.save(update_fields=["display_name"])

    social_account = SocialAccount.objects.create(
        user=user,
        provider=SocialProvider.GOOGLE,
        provider_user_id=provider_user_id,
        email=email,
    )
    return GoogleAuthResult(user=user, social_account=social_account, created=created)
