from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given email, username and password.
        """
        if not email:
            raise ValueError('The email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=32)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Profile(models.Model):
    picture = models.ImageField(null=True)
    username = models.CharField(max_length=50)
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, null=True)
    introduction = models.TextField()

    def __str__(self):
        return self.username


class Like(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    image = models.ForeignKey('photos.Photo', on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)
