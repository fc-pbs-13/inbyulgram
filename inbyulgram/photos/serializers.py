from rest_framework import serializers

from photos.models import Photo, Comment
from users.serializers import UserSerializer


class PhotoSerializer(serializers.ModelSerializer):
    user = UserSerializer

    class Meta:
        model = Photo
        fields = ['id', 'image', 'caption', 'posted_at', 'user']


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer
    Photo = PhotoSerializer

    class Meta:
        model = Comment
        fields = ['photo', 'comment_owner', 'description', 'commented_at',]