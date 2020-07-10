from rest_framework import viewsets

from photos.models import Photo
from photos.serializers import PhotoSerializer


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def get_queryset(self):
        return Photo.objects.filter(user=self.kwargs['users_pk'])
