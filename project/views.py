# Create your views here.
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from project.models import Project
from project.serializers import ProjectSerializer


class ProjectViewSet(ModelViewSet):
    """
    Query all Project
    Serialize all fields from Project
    Permission to define who can access the project
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        :return Make sure user is the author of the project:
        """
        return Project.objects.filter(author=self.request.user.id).order_by('id')

    def create(self, request, **kwargs):
        """
        :param request: Get data
        :param kwargs:
        :return: 201 if successful else 400
        """

        data = request.data.copy()
        data['author'] = request.user.id
        serialized_data = ProjectSerializer(data=data)
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()

        return Response(serialized_data.data, status=status.HTTP_201_CREATED)
