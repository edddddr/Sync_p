from __future__ import annotations

from rest_framework import mixins, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from apps.bookmarks.models import Bookmark
from apps.bookmarks.serializers import BookmarkSerializer
from apps.common.permissions import IsOwnerOrReadOnly


class BookmarkViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Bookmark.objects.none()
    serializer_class = BookmarkSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    filter_backends = (OrderingFilter,)
    ordering_fields = ("created_at",)
    ordering = ("-created_at",)

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Bookmark.objects.none()
        if not self.request.user.is_authenticated:
            return Bookmark.objects.none()

        return (
            Bookmark.objects.select_related("user", "post", "post__author", "post__place")
            .filter(user=self.request.user)
            .order_by("-created_at")
        )
