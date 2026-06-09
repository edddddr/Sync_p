from __future__ import annotations

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.ratings.views import PlaceRatingViewSet

router = DefaultRouter()
router.register("", PlaceRatingViewSet, basename="rating")

urlpatterns = [
    path("", include(router.urls)),
]
