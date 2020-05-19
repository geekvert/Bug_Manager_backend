from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from .serializers import *
from .models import *
from rest_framework import status, generics
from rest_framework.response import Response
import requests

from django.contrib.auth import login, logout

# from .permissions import *

# default permission class would be isAuthenticated

class BugViewSet(ModelViewSet):
    serializer_class = BugSerializer
    queryset = Bug.objects.all()

class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

class TagViewSet(ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

# Oauth wala view
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def Auth(request):
    client_id = 'er1eJX5UyeQgVLdDLICTjuUJKHogSrLRKfKLLIN9'
    client_secret = 'MQ4fR10F7Mti8aNMhoUKJfznpX6YwCCUffCzqrxHRDLuY9DIOZGgY3q16MVbnbbSFGrGnsXa40qOZB60twj5eK4n1OqMqExmIIOJCn0djXS57k8QAJ5OXPxndKB2E07M'
    desired_state = 'pypy'

    auth_code = request.query_params.get('code')
    state = request.query_params.get('state')

    if (state!=desired_state):
        return Response(
            data = 'Something went wrong, please try again later.',
            status = status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    url = 'https://internet.channeli.in/open_auth/token/'
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
        'redirect_url': 'http://127.0.0.1:8000/backend/test/',
        'code': auth_code
    }
    omni_data = requests.post(url=url, data=data).json()

    # checking for any errors
    if ('error' in  omni_data.keys()):
        return Response(
            data = omni_data['error'],
            status = status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # getting user_data
    access_token = omni_data['access_token']
    refresh_token = omni_data['refresh_token']
    headers = {
        'Authorization': 'Bearer '+access_token
    }
    user_data = requests.get(url='https://internet.channeli.in/open_auth/get_user_data/', headers=headers)

    # checking for any errors
    if (user_data.status_code!=200):
        return Response(
            data = user_data.json()['detail'],
            status = status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    user = user_data.json()

    # do you already exist?
    try:
        exist = User.objects.get(enrollment_no=user['student']['enrolmentNumber'])
    except:
        Response(
            data = 'You don\'t need to signup, user already exists.',
            status = status.HTTP_400_BAD_REQUEST
        )

    # are you an imgian?
    imgian = False
    for role in user['person']['roles']:
        if 'Maintainer' in role.values():
            imgian = True

    if not imgian:
        Response(
            data = 'You are not allowed to use this app as you are not an IMGIAN.',
            status = status.HTTP_401_UNAUTHORIZED
        )
    
    # are you an admin?
    admin_status = False
    if user['student']['currentYear'] > 3:
        admin_status = True

    # creating newUser if everything is fine
    enr_no = user['student']['enrolmentNumber']
    email = user['contactInformation']['instituteWebmailAddress']
    full_name = user['person']['fullName']
    fName = full_name.split()[0]

    try:
        newUser = User(username=full_name, email=email, enrollment_no=enr_no, first_name=fName, admin_status=admin_status, access_token=access_token, refresh_token=refresh_token)
        newUser.save()
        login(request=request, user=user)
    except:
        return Response(
            data = 'Unable to create account.',
            status = status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return Response(
        data = 'Voila! Account created successfully!',
        status = status.HTTP_200_OK
    )

class DisableUser(generics.UpdateAPIView):
    pass
# working viewsets

class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

class ProjectBugViewSet(ModelViewSet):
    serializer_class = BugSerializer

    # function to map project_names to their ids
    def nameMAPpk(self, project_name):
        id = Project.objects.get(name = project_name)
        return id

    def get_queryset(self):
        project_name = self.request.query_params.get('pName')
        queryset = Bug.objects.filter(project_id = self.nameMAPpk(project_name))
        return queryset

    def anon(self):
        return Response('data h ji data h')

class MyPage(ModelViewSet):
    serializer_class = BugSerializer

    # function to map usernames to their ids
    def nameMAPpk(self, my_name):
        id = User.objects.get(username = my_name)
        return id

    def get_queryset(self):
        my_name = self.request.query_params.get('my_name')
        query1 = Bug.objects.filter(reported_by = self.nameMAPpk(my_name))
        query2 = Bug.objects.filter(assigned_to = self.nameMAPpk(my_name))
        result = query1 | query2
        return result




@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def testView(request):
    return HttpResponse("Hello, World!")

@api_view(['GET', 'POST'])
def testing(request):
    if request.method == 'POST':
        return Response({"message": "Got some data!", "data": request.data})
    return Response(data = 'some message')