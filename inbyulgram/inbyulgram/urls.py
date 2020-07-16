"""inbyulgram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers

from photos.views import PhotoViewSet, CommentViewSet
from users.views import UserViewSet, ProfileViewSet, LikeViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'users', UserViewSet)
router.register(r'accounts', ProfileViewSet)

users_router = routers.NestedSimpleRouter(router, r'users', lookup='users')
users_router.register(r'photos', PhotoViewSet)
users_router.register(r'likes', LikeViewSet)

photo_router = routers.NestedSimpleRouter(users_router, r'photos', lookup='photos')
photo_router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^', include(users_router.urls)),
    url(r'^', include(photo_router.urls)),
]
