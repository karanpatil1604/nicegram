from django.urls import path
from .views import PostCreateView, PostDeleteView, PostUpdateView

urlpatterns = [
    path('create/', PostCreateView.as_view(), name="create-post"),
    path('update/', PostUpdateView.as_view(), name="update-post"),
    path('delete/', PostDeleteView.as_view(), name="delete-post"),
]
