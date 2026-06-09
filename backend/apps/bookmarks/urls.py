from __future__ import annotations

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.bookmarks.views import BookmarkViewSet

router = DefaultRouter()
router.register("", BookmarkViewSet, basename="bookmark")

urlpatterns = [
    path("", include(router.urls)),
]
