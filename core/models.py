from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    """Manager for custom user model to support email instead of username"""

    def create_user(self, email, password=None, **extra_args):
        """Creates and save the user with email instead of username"""
        if not email:
            raise ValueError('Users Must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_args)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        """Creates and saves new superuser"""
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Service(models.Model):
    """Service model to be used in index page"""
    name = models.CharField(max_length=60)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=128)
    body = models.TextField()

    def __str__(self):
        return self.name
