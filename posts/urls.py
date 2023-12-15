from django.urls import path
from .views import GetFollowerPosts, PostCreateView, PostDeleteView, PostUpdateView

urlpatterns = [
    path('feed/', GetFollowerPosts.as_view(), name="get-posts"),
    path('create/', PostCreateView.as_view(), name="create-post"),
    path('update/', PostUpdateView.as_view(), name="update-post"),
    path('delete/', PostDeleteView.as_view(), name="delete-post"),
]
