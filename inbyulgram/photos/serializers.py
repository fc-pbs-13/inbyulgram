from rest_framework import serializers

from photos.models import Photo, Comment
from users.serializers import UserSerializer, PhotoShowSerializer


class PhotoSerializer(serializers.ModelSerializer):
    user = PhotoShowSerializer(read_only=True)

    class Meta:
        model = Photo
        fields = ['id', 'image', 'caption', 'posted_at', 'user']


class CommentSerializer(serializers.ModelSerializer):
    user = PhotoShowSerializer(read_only=True)
    photo = PhotoSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'photo', 'user', 'description', 'commented_at', ]
