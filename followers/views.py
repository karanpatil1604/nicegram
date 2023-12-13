from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, DestroyAPIView
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
            return Response({"message": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        instance = Follower.objects.filter(
            follower=self.request.user, following=user_to_unfollow).first()

        if instance:
            instance.delete()
            return Response({"message": f"You have unfollowed user with ID {user_to_unfollow.id}."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "You are not following the specified user."}, status=status.HTTP_400_BAD_REQUEST)
