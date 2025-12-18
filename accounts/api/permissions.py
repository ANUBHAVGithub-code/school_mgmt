from rest_framework.permissions import BasePermission
class IsPrincipal(BasePermission):
    #allows access only to users in principal group.
    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False
        return user.groups.filter(name = 'Principal').exists() 
