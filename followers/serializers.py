from rest_framework import serializers
from .models import Follower


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ('follower',)
        extra_kwargs = {'follower': {'required': False}}


class FollowerFollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ('follower', 'following')
