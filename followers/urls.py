from django.urls import path
from .views import FollowUserView, UnfollowUserView


urlpatterns = [
    path('follow/', FollowUserView.as_view(), name="follow-user"),
    path('unfollow/',
         UnfollowUserView.as_view(), name="unfollow-user"),
]
