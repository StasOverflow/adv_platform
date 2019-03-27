from rest_framework import permissions


class IsTheUserOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if not request.user.is_superuser:
                if request.user.id != obj.id:
                    return False
        return True
