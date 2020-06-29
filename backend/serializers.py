from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'enrollment_no', 'admin_status', 'disabled_status']

class ProjectSerializer(serializers.ModelSerializer):
    team = serializers.StringRelatedField(many=True)
    creator = serializers.StringRelatedField()

    class Meta:
        model = Project
        fields= '__all__' # ['name', 'wiki', 'creator', 'team', 'timestamp']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields= '__all__'

# class SectorClassField(serializers.StringRelatedField):

#     def to_internal_value(self, value):
#         project = models.Projects.objects.filter(name=value)
#         if project and (len(sector_class)) == 1:
#             return sector_class.get().id
#         else:
#             raise serializers.ValidationError("Sector with name: %s not found" % value)

class TagSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()

    class Meta:
        model = Tag
        fields= '__all__'

class BugSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField()
    tags = serializers.StringRelatedField(many=True)
    # tags = TagSerializer(many=True)
    reported_by = serializers.StringRelatedField()
    assigned_to = serializers.StringRelatedField()

    class Meta:
        model = Bug
        fields = ['heading', 'description', 'status', 'reported_by', 'assigned_to', 'project', 'tags', 'timestamp']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
