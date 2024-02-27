"""
URL configuration for hoopToday project.

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
from django.urls import include, path
from rest_framework import routers

from django.contrib.auth.views import LoginView
from django.views.generic.base import RedirectView

from hooptoday import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns=[
    path('api/', views.api_root),

    path('', RedirectView.as_view(url='feed/', permanent=True)),

    path('users/', views.UserList.as_view(), name='users'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),

    path('posts/', views.PostList.as_view(), name = 'posts'),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name = 'post-detail'),

    path('feed/',views.PublicFeed.as_view(),name='feed'),
    path('createPost/',views.create_post_view,name='create-post'),
    path('createGamePost/',views.create_game_post_view,name='create-game-post'),

    path('signup/', views.signUp_view, name='signup'),
    path('login/', LoginView.as_view(
           template_name='loginUser.html',
           redirect_authenticated_user=True), name='login'),
    path('logout/', views.logout_view, name='logout'),
]


urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]

