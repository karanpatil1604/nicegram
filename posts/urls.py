from django.urls import path
from .views import all_posts

urlpatterns = [
    path('all-posts', all_posts, name='all-posts'),

]
