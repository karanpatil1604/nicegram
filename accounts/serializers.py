from rest_framework import serializers
from posts.models import Post

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'mobile',
                  'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            mobile=validated_data['mobile'],
            password=validated_data['password']
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'bio', 'profile_picture')


class UserWithPostSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'posts', 'bio', 'profile_picture')

    def get_posts(self, obj):
        from posts.serializers import PostSerializer
        posts = Post.objects.filter(author=obj)
        serializer = PostSerializer(posts, many=True)
        return serializer.data


class UserFeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'profile_picture')
