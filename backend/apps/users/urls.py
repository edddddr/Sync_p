from __future__ import annotations

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.users.views import MeView, RegisterView, UserViewSet

router = DefaultRouter()
router.register("users", UserViewSet, basename="user")

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="auth-register"),
    path("auth/me/", MeView.as_view(), name="auth-me"),
    path("", include(router.urls)),
]

