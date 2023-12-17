from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Follower
from accounts.models import User
from .serializers import FollowerSerializer


class FollowUserView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowerSerializer

    def perform_create(self, serializer):
        user_to_follow = get_object_or_404(
            User, id=self.request.data.get('user_id'))
        if self.request.user == user_to_follow:
            return Response({"message": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        if Follower.objects.filter(follower=self.request.user, following=user_to_follow).exists():
            return Response({"message": "You are already following this user."}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(follower=self.request.user, following=user_to_follow)
        return Response({"message": f"You are now following {user_to_follow.username}."}, status=status.HTTP_201_CREATED)


class UnfollowUserView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Follower.objects.filter(follower=self.request.user)

    def delete(self, request):
        user_to_unfollow = get_object_or_404(
            User, id=request.data.get('user_id'))
        if self.request.user == user_to_unfollow:
            print('same user')
            return Response({"message": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        instance = Follower.objects.filter(
            follower=self.request.user, following=user_to_unfollow).first()
        print(instance)
        if instance:
            instance.delete()
            return Response({"message": f"You have unfollowed user with ID {user_to_unfollow.id}."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "You are not following the specified user."}, status=status.HTTP_400_BAD_REQUEST)


class UserFollowing(ListAPIView):
    permission_classes = [IsAuthenticated]
    ueryset = User.objects.all()

    def get(self, request):
        query = request.query_params.get('id', '')
        user = get_object_or_404(User, id=query)
        if not query:
            return Response([], status=200)
        users = self.search_following(user)
        serialized_users = self.serialize_users(users)
        return Response(serialized_users, status=200)

    def search_following(self, user):
        users = User.objects.filter(
            id__in=Follower.objects.filter(follower=user).values('following__id'))
        return users

    def serialize_users(self, users):
        print('users aer ', users)
        serialized_users = [
            {'id': user.id, 'username': user.username} for user in users]
        return serialized_users
