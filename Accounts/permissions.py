from rest_framework.permissions import BasePermission


class UserPermissions(BasePermission):
    def has_permission(self, request, view=None):
        return request.user is not None


class AdminPermissions(BasePermission):
    def has_permission(self, request, view=None):
        user = request.user

        return user and user.is_admin == True


class SuperuserPermissions(BasePermission):
    def has_permission(self, request, view=None):
        user = request.user

        return user and user.is_superuser == True
