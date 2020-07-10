from django.db import models
from users.models import User


class Photo(models.Model):
    image = models.CharField(max_length=10)
    caption = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']
