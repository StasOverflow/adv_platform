from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.author_id == request.user.id


class IsAdminOrReadOnly(permissions.BasePermission):
    """Allow unsafe methods for admin users only."""

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if not request.user or not request.user.is_authenticated:
            if request.method in permissions.SAFE_METHODS:
                return True
            return False
        elif request.user.is_authenticated:
            return True