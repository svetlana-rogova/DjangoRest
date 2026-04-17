from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """
    Разрешение для пользователей с правами модератора.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True
        if request.user.groups.filter(name='moderator').exists():
            return True
        return False


class IsOwner(BasePermission):
    """
    Разрешение для владельца объекта.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.owner == request.user
