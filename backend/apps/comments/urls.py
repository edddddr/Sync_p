from __future__ import annotations

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.comments.views import CommentViewSet

router = DefaultRouter()
router.register("", CommentViewSet, basename="comment")

urlpatterns = [
    path("", include(router.urls)),
]
