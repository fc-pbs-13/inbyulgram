from django.db import models


class Photo(models.Model):
    image = models.CharField(max_length=10)
    caption = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['-id']


class Comment(models.Model):
    photo = models.ForeignKey('photos.Photo', on_delete=models.CASCADE, null=True)   # Null True > NOT NULL constraint failed:
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True)
    description = models.TextField()
    commented_at = models.DateTimeField(auto_now_add=True)
