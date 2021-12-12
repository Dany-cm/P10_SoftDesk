from rest_framework.serializers import ModelSerializer

from project.models import Project, Contributor, Issues, Comments


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        read_field_only = ['id', 'author']


class ContributorSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = '__all__'
        read_field_only = ['id', 'project']


class IssuesSerializer(ModelSerializer):
    class Meta:
        model = Issues
        fields = '__all__'
        read_field_only = ['id', 'project', 'author', 'created_time']


class CommentsSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'
        read_field_only = ['id', 'author', 'issue', 'created_time']
