from django.contrib.auth.models import AbstractUser
from django.db import models
from django_cryptography.fields import encrypt


# Create your models here.
class CustomUser(AbstractUser):
    first_name = encrypt(models.CharField(max_length=50))
    last_name = encrypt(models.CharField(max_length=50))
    email = encrypt(models.EmailField(max_length=50))
    password = models.CharField(max_length=50)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
