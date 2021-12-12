# Create your views here.
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from project.models import Project, Contributor
from project.serializers import ProjectSerializer, ContributorSerializer


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
        return Project.objects.filter(author=self.request.user).order_by('id')

    def create(self, request, *args, **kwargs):
        """
        :param request: Get data
        :param kwargs:
        :return: 201 if successful else 400
        """

        request.data["author"] = request.user.id
        return super(ProjectViewSet, self).create(request, *args, **kwargs)


class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Contributor.objects.filter(project_id=self.kwargs['project_pk']).order_by('id')

    def create(self, request, *args, **kwargs):
        try:
            contributor_list = []
            for contributor_user in Contributor.objects.filter(project_id=self.kwargs['project_pk']):
                contributor_list.append(contributor_user.user_id)

            if request.data['user'] in contributor_list:
                raise ValidationError("Le contributeur est déjà dans le projet")

        except Contributor.DoesNotExist:
            raise ValidationError("Le contributeur n'existe pas")
        else:
            request.data['project'] = self.kwargs['project_pk']
            return super(ContributorViewSet, self).create(request, *args, **kwargs)
