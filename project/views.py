# Create your views here.
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from project.models import Project, Contributor, Issues, Comments
from project.permissions import HasProjectPermissions, HasContributorPermissions, HasIssuePermissions, \
    HasCommentPermissions
from project.serializers import ProjectSerializer, ContributorSerializer, IssuesSerializer, CommentsSerializer


class ProjectViewSet(ModelViewSet):
    """
    Query all Project
    Serialize all fields from Project
    Permission to define who can access the project
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, HasProjectPermissions]

    def get_queryset(self):
        """
        :return Make sure user is the author of the project:
        """
        return Project.objects.filter(contributor__user=self.request.user).order_by('id')

    def create(self, request, *args, **kwargs):
        """
        :param request: Get data
        :param kwargs:
        :return: 201 if successful else 400
        """
        data = request.data.copy()
        data["author"] = request.user.id
        serialized_data = ProjectSerializer(data=data)
        serialized_data.is_valid(raise_exception=True)
        project = serialized_data.save()

        contributor = Contributor.objects.create(user=request.user, project=project, role='AUTHOR')
        contributor.save()

        return Response(serialized_data.data, status=status.HTTP_201_CREATED)


class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, HasContributorPermissions]

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


class IssuesViewSet(ModelViewSet):
    serializer_class = IssuesSerializer
    permission_classes = [IsAuthenticated, HasIssuePermissions]

    def get_queryset(self):
        return Issues.objects.filter(project=self.kwargs['project_pk']).order_by('id')

    def create(self, request, *args, **kwargs):
        request.data["author"] = request.user.id
        request.data["project"] = kwargs["project_pk"]
        return super(IssuesViewSet, self).create(request, *args, **kwargs)


class CommentsViewSet(ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated, HasCommentPermissions]

    def get_queryset(self):
        return Comments.objects.filter(issue=self.kwargs['issue_pk']).order_by('id')

    def create(self, request, *args, **kwargs):
        request.data["author"] = request.user.pk
        request.data["issue"] = kwargs["issue_pk"]
        return super(CommentsViewSet, self).create(request, *args, **kwargs)
