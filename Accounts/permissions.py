from rest_framework.permissions import BasePermission


class UserPermissions(BasePermission):
    def has_permission(self, request, view=None):
        print(request)
        return request.user and request.user != None


class AdminPermissions(BasePermission):
    def has_permission(self, request, view=None):
        print(request)
        user = request.user

        return user and user.is_admin == True


class SuperuserPermissions(BasePermission):
    def has_permission(self, request, view=None):
        print(request)
        user = request.user

        return user and user.is_superuser == True
