from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from accounts.models import User
from followers.models import Follower
from .serializers import PostSerializer, PostUpdateSerializer, PostWithAuthorSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Post


class GetFollowerPosts(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        following_users = Follower.objects.filter(
            follower=request.user).values_list('following', flat=True)

        posts = Post.objects.filter(
            author__in=following_users).order_by('-created')
        serializer = PostWithAuthorSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            post = serializer.save(author=request.user)
            response_data = {
                "post_id": post.post_id,
                "picture": str(post.picture),
                "caption": post.caption,
                "author_id": post.author.id
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        post_id = request.data.get('post_id')
        if not post_id:
            return Response({"error": "post_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            post = Post.objects.get(post_id=post_id, author=request.user)
        except Post.DoesNotExist:
            return Response({"error": "Post does not exist"}, status=status.HTTP_404_NOT_FOUND)
        if post:
            serializer = PostUpdateSerializer(post, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        post_id = request.data.get('post_id')
        if not post_id:
            return Response({"error": "post_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            post = Post.objects.get(post_id=post_id, author=request.user)
        except Post.DoesNotExist:
            return Response({"error": "Post does not exist"}, status=status.HTTP_404_NOT_FOUND)
        if post:
            post.delete()
            return Response("Post deleted successfully", status=status.HTTP_200_OK)
        else:
            return Response({"error": "Post does not exist"}, status=status.HTTP_404_NOT_FOUND)


# def all_posts(request):
#     posts = [
#         {
#             "id": 1,
#             "image": "url_for the image",
#             "caption": "Image caption 1",
#             "user_id": 2
#         },
#         {
#             "id": 2,
#             "image": "url_for the image2",
#             "caption": "Image caption 3",
#             "user_id": 1
#         },
#         {
#             "id": 3,
#             "image": "url_for the image4",
#             "caption": "Image caption 3",
#             "user_id": 2
#         },
#     ]
#     response_data = {'posts': posts}
#     return JsonResponse(response_data)
