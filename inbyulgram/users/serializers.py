from rest_framework import serializers

from users.models import User, Profile, Like


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # user = super(UserSerializer, self).create(validated_data)
        return User.objects.create_user(**validated_data)


class PhotoShowSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField(use_url=True, source='profile.picture')

    class Meta:
        model = User
        fields = ['id', 'username', 'picture']


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


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'image']
        read_only_fields = ['id', 'user', ]