from rest_framework import viewsets

from photos.models import Photo, Comment
from photos.serializers import PhotoSerializer, CommentSerializer


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def get_queryset(self):
        return Photo.objects.filter(user=self.kwargs['users_pk'])


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    # def get_queryset(self):
    #     return Comment.objects.filter(user=self.kwargs['photo_pk'])
