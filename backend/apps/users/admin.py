from __future__ import annotations

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from apps.users.models import Follow, SocialAccount, User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ("id", "email", "username", "display_name", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active", "date_joined")
    search_fields = ("email", "username", "display_name")
    ordering = ("-date_joined",)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2"),
            },
        ),
    )

    fieldsets = DjangoUserAdmin.fieldsets + (
        (
            "Profile",
            {
                "fields": (
                    "display_name",
                    "bio",
                    "avatar",
                    "location",
                    "website",
                )
            },
        ),
    )


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("id", "follower", "following", "created_at")
    search_fields = ("follower__email", "following__email")
    autocomplete_fields = ("follower", "following")


@admin.register(SocialAccount)
class SocialAccountAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "provider", "email", "created_at")
    list_filter = ("provider", "created_at")
    search_fields = ("user__email", "user__username", "provider_user_id", "email")
    autocomplete_fields = ("user",)
