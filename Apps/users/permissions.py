from rest_framework import permissions


class IsRoleUser(permissions.BasePermission):
    def has_permission(self, request, view):
        required_roles = getattr(view, 'required_roles', [])
        user_roles = [role.nome for role in request.user.roles.all()]
        return any(role in user_roles for role in required_roles )