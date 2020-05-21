from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'enrollment_no', 'admin_status', 'disabled_status', 'access_token', 'refresh_token']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields= '__all__' # ['name', 'wiki', 'creator', 'team', 'timestamp']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields= '__all__'

class BugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bug
        fields= '__all__' # ['heading', 'description', 'status', 'reported_by', 'assigned_to', 'project', 'tags', 'timestamp']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields= '__all__'
