from __future__ import annotations

from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.comments.models import Comment
from apps.comments.serializers import CommentSerializer
from apps.common.permissions import IsOwnerOrReadOnly


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ("post", "author")
    ordering_fields = ("created_at", "updated_at")
    ordering = ("created_at",)

    def get_queryset(self):
        queryset = Comment.objects.select_related("author", "post", "post__author")

        if self.request.user.is_authenticated:
            return queryset.filter(
                Q(post__is_public=True)
                | Q(post__author=self.request.user)
                | Q(author=self.request.user)
            )

        return queryset.filter(post__is_public=True)
