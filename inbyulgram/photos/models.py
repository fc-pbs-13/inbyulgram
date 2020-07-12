from django.contrib.auth.models import User
from django.db import models


class Photo(models.Model):
    image = models.CharField(max_length=10)
    caption = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']


class Comment(models.Model):
    photo = models.ForeignKey('Photo', on_delete=models.CASCADE)
    comment_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    commented_at = models.DateTimeField(auto_now_add=True)

