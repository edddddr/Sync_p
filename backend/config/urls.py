from __future__ import annotations

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from config.views import health_check

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health/", health_check, name="health-check"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("api/auth/token/verify/", TokenVerifyView.as_view(), name="token-verify"),
    path("api/auth/logout/", TokenBlacklistView.as_view(), name="token-blacklist"),
    path("api/", include("apps.users.urls")),
    path("api/places/", include("apps.places.urls")),
    path("api/posts/", include("apps.posts.urls")),
    path("api/comments/", include("apps.comments.urls")),
    path("api/ratings/", include("apps.ratings.urls")),
    path("api/bookmarks/", include("apps.bookmarks.urls")),
    path("api/notifications/", include("apps.notifications.urls")),
]
