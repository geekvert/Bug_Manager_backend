from rest_framework import serializers
from .models import *
from collections import OrderedDict

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'enrollment_no', 'admin_status', 'disabled_status']

class AltStringRelatedField(serializers.StringRelatedField):
    def to_internal_value(self, value):
        user = User.objects.get(username=value)
        return user.id

class ProjectSerializer(serializers.ModelSerializer):
    team = AltStringRelatedField(many=True)
    creator = serializers.StringRelatedField()

    class Meta:
        model = Project
        fields= '__all__' # ['name', 'wiki', 'creator', 'team', 'timestamp']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields= '__all__'

class TagSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()

    class Meta:
        model = Tag
        fields= '__all__'

class TagStringRelatedField(serializers.StringRelatedField):
    def to_internal_value(self, value):
        tag = Tag.objects.get(name=value)
        return tag.id

class BugSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField()
    tags = TagStringRelatedField(many=True)
    reported_by = serializers.StringRelatedField()
    assigned_to = serializers.StringRelatedField()

    class Meta:
        model = Bug
        fields = ['heading', 'description', 'status', 'reported_by', 'assigned_to', 'project', 'tags', 'timestamp']

    # def update(self, instance, validated_data):
    #     print(repr(validated_data), repr(self.data))
    #     return instance

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
