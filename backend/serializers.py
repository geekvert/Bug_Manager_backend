from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()
    team = serializers.StringRelatedField(many=True)

    class Meta:
        model = Project
        fields= ['name', 'wiki', 'creator', 'team', 'timestamp']    # expt try '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields= '__all__'

class BugSerializer(serializers.ModelSerializer):
    reported_by = serializers.StringRelatedField()
    assigned_to = serializers.StringRelatedField()
    project = serializers.StringRelatedField()
    tags = serializers.StringRelatedField(many=True)

    class Meta:
        model = Bug
        fields= ['heading', 'description', 'status', 'reported_by', 'assigned_to', 'project', 'tags', 'timestamp']

class CommentSerializer(serializers.ModelSerializer):
    bug = serializers.StringRelatedField()
    commentator = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['body', 'bug', 'commentator']

class TagSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()

    class Meta:
        model = Tag
        fields= ['name', 'creator']
