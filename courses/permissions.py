from rest_framework.permissions import BasePermission


class IsNotModeratorForAPIView(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='moderators'):
            return False
        return True


class IsNotModeratorForViewSet(BasePermission):
    def has_permission(self, request, view):
        if view.action in ['create', 'destroy']:
            if request.user.groups.filter(name='moderators'):
                return False
            return True
        return True


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner or request.user.is_staff:
            return True
        return False
