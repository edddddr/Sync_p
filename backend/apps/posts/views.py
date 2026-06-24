from __future__ import annotations

from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.bookmarks.services import bookmark_post, unbookmark_post
from apps.comments.serializers import CommentSerializer
from apps.common.permissions import IsOwnerOrReadOnly
from apps.posts.models import Post
from apps.posts.serializers import PostReadSerializer, PostWriteSerializer
from apps.posts.services import like_post, unlike_post


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ("author", "place", "is_public")
    search_fields = ("caption", "author__username", "place__name", "place__city", "place__country")
    ordering_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)

    def get_queryset(self):
        queryset = Post.objects.select_related(
            "author",
            "place",
            "place__created_by",
        ).prefetch_related("images")

        if self.request.user.is_authenticated:
            return queryset.filter(Q(is_public=True) | Q(author=self.request.user))

        return queryset.filter(is_public=True)

    def get_serializer_class(self):
        if self.action in {"create", "update", "partial_update"}:
            return PostWriteSerializer
        return PostReadSerializer

    @action(detail=False, methods=["get"])
    def explore(self, request):
        queryset = self.get_queryset().filter(is_public=True).order_by("-created_at")
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], permission_classes=(IsAuthenticated,))
    def like(self, request, pk=None):
        post = self.get_object()
        like, created = like_post(user=request.user, post=post)
        return Response(
            {
                "id": like.id,
                "post": post.id,
                "created": created,
                "likes_count": post.likes.count(),
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], permission_classes=(IsAuthenticated,))
    def unlike(self, request, pk=None):
        post = self.get_object()
        deleted_count = unlike_post(user=request.user, post=post)
        return Response(
            {
                "deleted": deleted_count > 0,
                "likes_count": post.likes.count(),
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], permission_classes=(IsAuthenticated,))
    def bookmark(self, request, pk=None):
        post = self.get_object()
        bookmark, created = bookmark_post(user=request.user, post=post)
        return Response(
            {
                "id": bookmark.id,
                "post": post.id,
                "created": created,
                "bookmarks_count": post.bookmarks.count(),
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], permission_classes=(IsAuthenticated,))
    def unbookmark(self, request, pk=None):
        post = self.get_object()
        deleted_count = unbookmark_post(user=request.user, post=post)
        return Response(
            {
                "deleted": deleted_count > 0,
                "bookmarks_count": post.bookmarks.count(),
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["get", "post"], permission_classes=(IsAuthenticatedOrReadOnly,))
    def comments(self, request, pk=None):
        post = self.get_object()

        if request.method == "POST":
            data = request.data.copy()
            data["post_id"] = post.id
            serializer = CommentSerializer(data=data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        queryset = post.comments.select_related("author").order_by("created_at")
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = CommentSerializer(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)

        serializer = CommentSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)
