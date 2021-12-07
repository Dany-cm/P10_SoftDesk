from django.conf import settings
from django.db import models


# Create your models here.
class Project(models.Model):
    TYPE_CHOICES = [('BACKEND', 'BACKEND'), ('FRONTEND', 'FRONTEND'), ('IOS', 'IOS'), ('ANDROID', 'ANDROID')]

    title = models.CharField(max_length=128)
    description = models.TextField(max_length=1024)
    type = models.CharField(choices=TYPE_CHOICES, max_length=128)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='author', on_delete=models.CASCADE)
