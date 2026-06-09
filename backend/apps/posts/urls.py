from __future__ import annotations

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.posts.views import PostViewSet

router = DefaultRouter()
router.register("", PostViewSet, basename="post")

urlpatterns = [
    path("", include(router.urls)),
]
