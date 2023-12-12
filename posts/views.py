from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.


def all_posts(request):
    posts = [
        {
            "id": 1,
            "image": "url_for the image",
            "caption": "Image caption 1",
            "user_id": 2
        },
        {
            "id": 2,
            "image": "url_for the image2",
            "caption": "Image caption 3",
            "user_id": 1
        },
        {
            "id": 3,
            "image": "url_for the image4",
            "caption": "Image caption 3",
            "user_id": 2
        },
    ]
    response_data = {'posts': posts}
    return JsonResponse(response_data)
