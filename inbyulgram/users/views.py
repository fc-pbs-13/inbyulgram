from rest_framework import viewsets
from rest_framework.decorators import action

from users.models import Profile, User
from users.serializers import UserSerializer, ProfileUpdateSerializer, ProfileCreateSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action()
    def login(self, request):
        """
        - 회원 가입이 된 유저 >> 유저네임, 이메일, 패스워드
        - 를 활용하여 해당 유저가 올바르게 로그인 되었는지 확인하고
        - 올바르게 로그인 된 유저라면
        token, created = Token.objects.get_or_create(user=user)
        이 코드를 적절히 활용해서, 토큰을 되돌려 주는 로직을 작성.
        """
        pass

    def logout(self, request):
        """
        self.request.user 를 하면, 해당 로그인(토큰 발급) 된 유저를 장고에서 알아서 찾아준다.
        이 user는 토큰을 가지고 있다. 토큰을 삭제하는 로직을 작성.
        - 디버거를 적절히 잘 활용해서, 해당 토큰을 삭제해준다.
        - 토큰이 삭제가 된 후, response로 올바르게 삭제가 되었음을 알려준다.
        """
        pass

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileUpdateSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return ProfileCreateSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
