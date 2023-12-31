from ast import List, Not
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from followers.models import Follower

from posts import serializers
from .serializers import UserFeedSerializer, UserSerializer, UserProfileSerializer, UserWithPostSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.db import models
from .models import User


class UserSignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            # token, created = Token.objects.get_or_create(user=user)

            response_ = {
                "message": "User created successfully",
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
            }
            # "token": token.key
            return Response(response_, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(
            request, username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)

            response_data = {
                "message": "Login successful",
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "mobile": user.mobile,
                "token": token.key,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username=None):
        user = None
        if username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            user = request.user
        if user:
            serializer = UserProfileSerializer(user)
        else:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        permission_classes = [IsAuthenticated]
        user = get_object_or_404(User, id=request.data.get('user_id'))
        serializer = UserWithPostSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserProfileEditView(UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSearchView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response([], status=200)
        users = self.search_users(query)
        serialized_users = self.serialize_users(users)
        return Response(serialized_users, status=200)

    # def post(self, request):
    #     query = request.data.get('q', '')
    #     print(query, "this is qury")
    #     users = self.search_users(query)
    #     serialized_users = self.serialize_users(users)
    #     return Response(serialized_users, status=200)

    def search_users(self, query):
        users = User.objects.filter(
            models.Q(username__icontains=query) |
            models.Q(email__icontains=query) |
            models.Q(mobile__icontains=query)
        )
        return users

    def serialize_users(self, users):
        serialized_users = [
            {'id': user.id, 'username': user.username} for user in users]
        return serialized_users


class SuggestedUserView(ListAPIView):
    permission_classes = [IsAuthenticated]
    # serializer_class = UserFeedSerializer

    def get(self, request):
        current_user = request.user
        try:
            users_not_followed = User.objects.exclude(
                id__in=Follower.objects.filter(
                    follower=current_user).values('following__id')
            ).exclude(id=current_user.id)[:8]
        except:
            return Response({'message': 'No users to suggest'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserFeedSerializer(users_not_followed, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def get_queryset(self):
    #     current_user = self.request.user
    #     print('hello', current_user)
    #     users_not_followed = User.objects.exclude(
    #         id__in=Follower.objects.filter(
    #             follower=current_user).values('following__id')
    #     )

    #     return users_not_followed
