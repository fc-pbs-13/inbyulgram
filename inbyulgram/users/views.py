from django.contrib.auth import authenticate
from rest_framework import viewsets, status, mixins
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from users.models import Profile, User, Like
from users.permnissions import UserPermissions
from users.serializers import UserSerializer, ProfileUpdateSerializer, ProfileCreateSerializer, LikeSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserPermissions]

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(email=email, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'email': user.email}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'User Does Not Exist.'}, status=status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['delete'])
    def logout(self, request):
        request.user.auth_token.delete()
        return Response({"message": "Successfully Log Out."}, status.HTTP_200_OK)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileUpdateSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return ProfileCreateSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LikeViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [UserPermissions]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(user=request.user.id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)