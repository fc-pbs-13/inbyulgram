from django.contrib.auth.models import User
from django.db import models


#
# class User(models.Model):
#     email = models.EmailField(max_length=254)
#     password = models.CharField(max_length=32)
#
#     def __str__(self):
#         return self.email


class Profile(models.Model):
    picture = models.ImageField(null=True)
    username = models.CharField(max_length=50)
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, null=True)
    introduction = models.TextField()

    def __str__(self):
        return self.username
