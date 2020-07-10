from rest_framework import serializers

from photos.models import Photo
from users.serializers import UserSerializer


class PhotoSerializer(serializers.ModelSerializer):
    user = UserSerializer

    class Meta:
        model = Photo
        fields = ['id', 'image', 'caption', 'posted_at', 'user']
