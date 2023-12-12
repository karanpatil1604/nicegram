from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, username, email, mobile, password=None, **extra_fields):
        if not mobile:
            raise ValueError('The Mobile field must be set')
        if not username:
            raise ValueError('The username field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, mobile=mobile,
                          email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):
    objects = UserManager()
    username = models.CharField(
        max_length=150, unique=True, null=False, blank=False)
    mobile = models.CharField(
        max_length=15, unique=True, null=False, blank=False)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/', null=True, blank=True)
