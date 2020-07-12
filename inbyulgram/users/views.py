from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response

from users.models import Profile, User
from users.serializers import UserSerializer, ProfileUpdateSerializer, ProfileCreateSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            login(request, user)
            return Response({'token': token.key, 'email': user.email}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'User Does Not Exist.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['delete'])
    def logout(self, request):
        try:
            request.user.quth_token.delete()
            return Response({"message": "Successfully Log Out."}, status.HTTP_200_OK)
        except (AttributeError, ObjectDoesNotExist):
            return Response({"message": "Not Authorized User."}, status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileUpdateSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return ProfileCreateSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
