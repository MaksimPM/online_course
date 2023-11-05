from rest_framework.permissions import BasePermission


class IsOwnerProfile(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj or request.user.is_staff:
            return True
        return False
