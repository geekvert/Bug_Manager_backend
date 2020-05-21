import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import *
from .models import *
from .permissions import *
from django.contrib.auth import login, logout

from django.http import HttpResponse
from rest_framework.decorators import action

# homepage
class ProjectViewSet(ModelViewSet):
    lookup_field = 'name'
    # permission_classes = [CreatorTeamAdminPermission]
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

# project_page, bug_page
class ProjectBugViewSet(ModelViewSet):
    serializer_class = BugSerializer
    lookup_field = 'heading'
    # permission_classes = [CreatorTeamAdminPermission]

    # function to map project_names to their ids
    def nameMAPpk(self, project_name):
        id = Project.objects.get(name = project_name)
        return id

    def get_queryset(self):
        project_name = self.request.query_params.get('project_name')
        queryset = Bug.objects.filter(project_id = self.nameMAPpk(project_name))
        return queryset

# my_page
class MyPage(ModelViewSet):
    serializer_class = BugSerializer
    # permission_classes = [IsAuthenticated]

    # function to map usernames to their ids
    def nameMAPpk(self, my_name):
        id = User.objects.get(username = my_name)
        return id

    def get_queryset(self):
        my_name = self.request.query_params.get('my_name')
        query1 = Bug.objects.filter(reported_by = self.nameMAPpk(my_name))
        query2 = Bug.objects.filter(assigned_to = self.nameMAPpk(my_name))
        return query1 | query2

# admin_page
class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AdminPermission]
    lookup_field = 'enrollment_no'