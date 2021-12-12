from rest_framework.serializers import ModelSerializer

from project.models import Project, Contributor


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
