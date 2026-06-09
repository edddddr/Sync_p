from __future__ import annotations

from django.db.models import Avg, Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.common.permissions import IsOwnerOrReadOnly
from apps.places.models import Place
from apps.places.serializers import PlaceSerializer


class PlaceViewSet(viewsets.ModelViewSet):
    serializer_class = PlaceSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ("category", "city", "country")
    search_fields = ("name", "address", "city", "country")
    ordering_fields = ("name", "created_at", "posts_count")
    ordering = ("name",)
    lookup_field = "slug"

    def get_queryset(self):
        return (
            Place.objects.select_related("created_by")
            .annotate(
                posts_count=Count("posts", filter=Q(posts__is_public=True), distinct=True),
                ratings_count=Count("ratings", distinct=True),
                average_rating=Avg("ratings__score"),
            )
            .order_by("name")
        )

    @action(detail=False, methods=["get"])
    def trending(self, request):
        queryset = (
            self.get_queryset()
            .filter(posts_count__gt=0)
            .order_by("-posts_count", "-created_at")
        )
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
