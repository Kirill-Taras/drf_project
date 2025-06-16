from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsModer(BasePermission):
    """Проверяет, является ли пользователь модератором"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name="moders").exists()


class IsOwner(BasePermission):
    """Проверяет, является ли пользователь владельцем объекта"""

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsOwnerOrModer(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    """Разрешает редактирование только владельцу, но чтение всем"""

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.groups.filter(name="moders").exists():
            return request.method in ["PUT", "PATCH"]
        return obj.owner == request.user
