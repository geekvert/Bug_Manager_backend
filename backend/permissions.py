from rest_framework import permissions

# for projectviewset, projectBugviewset
class CreatorTeamAdminPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or request.method == 'POST':
            return True
        cta = request.user in obj.team or request.user == obj.creator or request.user.admin_status # team or creator or admin
        return cta

# for userviewset
class AdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.admin_status:
            return True
        False