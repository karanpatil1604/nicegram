from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    mobile = models.CharField(
        max_length=15, unique=True, null=True, blank=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/', null=True, blank=True)
