from rest_framework import permissions
from .models import *

# for projectviewset, projectBugviewset
class CreatorTeamAdminPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or request.method == 'POST':
            return True
        acs_token = request.headers['Authorization'].split(' ')[1]
        user = getUser(acs_token)
        if isinstance(obj, Project):
            cta = user.admin_status or user == obj.creator or user in obj.team # team or creator or admin
            return cta
        else:
            cta = user.admin_status or user == obj.project.creator or user in obj.project.team # team or creator or admin
            return cta

# for userviewset
class AdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS or request.method == 'POST':
            return True
        acs_token = request.headers['Authorization'].split(' ')[1]
        user = getUser(acs_token)
        if user.admin_status:
            return True
        return False

# default permission class
class NotDisabled(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        acs_token = request.headers['Authorization'].split(' ')[1]
        user = getUser(acs_token)
        if user.disabled_status:
            return False
        return True

# returns a user corresponding to an access_token
def getUser(acs_token):
    user = User.objects.get(access_token=acs_token)
    return user
