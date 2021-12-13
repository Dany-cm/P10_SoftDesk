from rest_framework.permissions import BasePermission, SAFE_METHODS

from project.models import Project


class HasProjectPermissions(BasePermission):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user == obj.author


class HasContributorPermissions(BasePermission):

    def has_permission(self, request, view):
        project = Project.objects.get(id=view.kwargs['project_pk'])
        if project in Project.objects.filter(contributor__user=request.user):
            project = Project.objects.get(id=view.kwargs['project_pk'])
            if request.method in SAFE_METHODS:
                return True
            return request.user == project.author
        return False


class HasIssuePermissions(BasePermission):

    def has_permission(self, request, view):
        project = Project.objects.get(id=view.kwargs['project_pk'])
        if project in Project.objects.filter(contributor__user=request.user):
            return True
        return False


class HasCommentPermissions(BasePermission):

    def has_permission(self, request, view):
        project = Project.objects.get(id=view.kwargs['project_pk'])
        if project in Project.objects.filter(contributor__user=request.user):
            return True
        return False
