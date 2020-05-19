from rest_framework import permissions

# obj would be project

class AdminOrProjectCreator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if(request.method in permissions.SAFE_METHODS) or (request.method == 'POST'):
            return True
        return (obj.creator == request.user) or request.user.admin_status

class TeamMemberOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if(request.method in permissions.SAFE_METHODS) or (request.method == 'POST'):
            return True
        return (request.user in obj.team.all()) or request.user.admin_status
