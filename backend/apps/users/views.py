from __future__ import annotations

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.users.models import User
from apps.users.serializers import RegisterSerializer, UserProfileSerializer, UserPublicSerializer
from apps.users.services import follow_user, unfollow_user


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)


class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self) -> User:
        return self.request.user


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserPublicSerializer
    permission_classes = (AllowAny,)
    filter_backends = (SearchFilter,)
    search_fields = ("username", "display_name")
    lookup_field = "id"

    def get_queryset(self):
        return User.objects.filter(is_active=True).order_by("-date_joined")

    @action(detail=True, methods=["post"], permission_classes=(IsAuthenticated,))
    def follow(self, request, id=None):
        user = self.get_object()

        try:
            follow, created = follow_user(follower=request.user, following=user)
        except DjangoValidationError as exc:
            raise ValidationError(exc.messages) from exc

        return Response(
            {
                "id": follow.id,
                "following": UserPublicSerializer(user, context={"request": request}).data,
                "created": created,
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], permission_classes=(IsAuthenticated,))
    def unfollow(self, request, id=None):
        user = self.get_object()
        deleted_count = unfollow_user(follower=request.user, following=user)
        return Response({"deleted": deleted_count > 0}, status=status.HTTP_200_OK)
