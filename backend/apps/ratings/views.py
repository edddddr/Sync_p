from __future__ import annotations

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.common.permissions import IsOwnerOrReadOnly
from apps.ratings.models import PlaceRating
from apps.ratings.serializers import PlaceRatingSerializer


class PlaceRatingViewSet(viewsets.ModelViewSet):
    serializer_class = PlaceRatingSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ("place", "user", "score")
    ordering_fields = ("created_at", "updated_at", "score")
    ordering = ("-updated_at",)

    def get_queryset(self):
        return PlaceRating.objects.select_related("user", "place", "place__created_by")
