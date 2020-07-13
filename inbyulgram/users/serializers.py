from rest_framework import serializers

from users.models import User, Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', ]
        extra_kwargs = {'password': {'write_only': True}}


class ProfileUpdateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['picture', 'username', 'user', 'introduction', ]
        read_only_fields = ['user']

    def create(self, validated_data):
        pass

class ProfileCreateSerializer(serializers.ModelSerializer):
    # user = UserSerializer

    class Meta:
        model = Profile
        fields = ['picture', 'username', 'user', 'introduction', ]
