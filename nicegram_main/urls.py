"""
URL configuration for nicegram_main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from urllib import request
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static


def hello(request):
    return "<h1>Hello World</h1>"


urlpatterns = [
    path('', hello, name="homepage"),
    path('admin/', admin.site.urls),
    path('post/', include('posts.urls')),
    path('user/', include('accounts.urls')),
    path('users/', include('followers.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
