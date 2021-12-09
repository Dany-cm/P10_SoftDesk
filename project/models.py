from django.conf import settings
from django.db import models


# Create your models here.
class Project(models.Model):
    TYPE_CHOICES = [('BACKEND', 'BACKEND'), ('FRONTEND', 'FRONTEND'), ('IOS', 'IOS'), ('ANDROID', 'ANDROID')]

    title = models.CharField(max_length=128)
    description = models.TextField(max_length=1024)
    type = models.CharField(choices=TYPE_CHOICES, max_length=128)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='author', on_delete=models.CASCADE)


class Contributor(models.Model):
    ROLE = [('AUTHOR', 'AUTHOR'), ('CONTRIBUTOR', 'CONTRIBUTOR')]

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name='contributor')
    role = models.CharField(choices=ROLE, max_length=128)


class Issues(models.Model):
    TYPE_PRIORITY = [('LOW', 'LOW'), ('MEDIUM', 'MEDIUM'), ('HIGH', 'HIGH')]
    TYPE_TAG = [('BUG', 'BUG'), ('IMPROVEMENT', 'IMPROVEMENT'), ('TASK', 'TASK')]
    TYPE_STATUS = [('TODO', 'TODO'), ('IN PROGRESS', 'IN PROGRESS'), ('COMPLETED', 'COMPLETED')]

    title = models.CharField(max_length=128)
    desc = models.CharField(max_length=1024)
    tag = models.CharField(choices=TYPE_TAG, max_length=128)
    priority = models.CharField(choices=TYPE_PRIORITY, max_length=128)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    status = models.CharField(choices=TYPE_STATUS, max_length=128)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assignee = models.ForeignKey(default="CONTRIBUTOR", to=Contributor, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)


class Comments(models.Model):
    description = models.CharField(max_length=128)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue = models.ForeignKey(to=Issues, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
