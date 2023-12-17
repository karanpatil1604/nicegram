from django.urls import path
from .views import FollowUserView, UnfollowUserView, UserFollowing


urlpatterns = [
    path('follow/', FollowUserView.as_view(), name="follow-user"),
    path('unfollow/',
         UnfollowUserView.as_view(), name="unfollow-user"),
    path('following/', UserFollowing.as_view(), name='user-following')
]
