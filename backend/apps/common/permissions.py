from __future__ import annotations

from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """Allow public reads, but only the owning user can mutate an object."""

    owner_fields = ("author", "created_by", "user")

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in SAFE_METHODS:
            return True

        if not request.user or not request.user.is_authenticated:
            return False

        return any(getattr(obj, field, None) == request.user for field in self.owner_fields)

