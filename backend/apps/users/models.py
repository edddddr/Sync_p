from __future__ import annotations

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Q


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email: str, password: str | None, **extra_fields):
        if not email:
            raise ValueError("The email field must be set.")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str | None = None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str | None = None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(unique=True)
    display_name = models.CharField(max_length=80, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    location = models.CharField(max_length=120, blank=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    class Meta:
        ordering = ("-date_joined",)
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self) -> str:
        return self.display_name or self.username or self.email


class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following_relationships",
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower_relationships",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["follower", "following"]),
            models.Index(fields=["following"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=("follower", "following"),
                name="unique_follow_relationship",
            ),
            models.CheckConstraint(
                check=~Q(follower=F("following")),
                name="prevent_self_follow",
            ),
        ]

    def clean(self) -> None:
        if self.follower_id == self.following_id:
            raise ValidationError("Users cannot follow themselves.")

    def __str__(self) -> str:
        return f"{self.follower} follows {self.following}"


class SocialProvider(models.TextChoices):
    GOOGLE = "google", "Google"
    APPLE = "apple", "Apple"


class SocialAccount(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="social_accounts",
    )
    provider = models.CharField(max_length=32, choices=SocialProvider.choices)
    provider_user_id = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("provider", "created_at")
        indexes = [
            models.Index(fields=["provider", "provider_user_id"], name="users_social_provider_uid_idx"),
            models.Index(fields=["email"], name="users_social_email_idx"),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=("provider", "provider_user_id"),
                name="unique_social_account_provider_user",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.provider}:{self.provider_user_id}"
