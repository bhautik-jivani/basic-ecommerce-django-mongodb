from rest_framework.permissions import BasePermission

from user_app.models import User

class HasPermission(BasePermission):
    message = "You are not authorized to perform this action"

    def has_permission(self, request, view):
        try:
            user = User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            return False
        
        user_roles = user.roles
        if not user_roles:
            user_roles = []

        required_permissions = getattr(view, 'permission_required', [])
        user_permissions = set(p.name for role in user_roles for p in role.permissions )
        # return any(perm in user_permissions for perm in required_permissions)

        for perm in required_permissions:
            if request.method == "GET" and ("view" in perm or "*" in perm) and perm in user_permissions:
                return True
            elif request.method == "POST" and ("add" in perm or "*" in perm) and perm in user_permissions:
                return True
            elif request.method == "PUT" and ("update" in perm or "*" in perm) and perm in user_permissions:
                return True
            elif request.method == "PATCH" and ("update" in perm or "*" in perm) and perm in user_permissions:
                return True
            elif request.method == "DELETE" and ("delete" in perm or "*" in perm) in perm and perm in user_permissions:
                return True
        return False
    
    def has_object_permission(self, request, view, obj):
        if not self.has_permission(request, view):
            return False
        return True
