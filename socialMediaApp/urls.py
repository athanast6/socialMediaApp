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

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth.views import LoginView
from django.views.generic.base import RedirectView

from django.contrib import admin


from hooptoday import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns=[
    path('api/', views.api_root),

    path('admin/', admin.site.urls),

    path('', views.about),

    path('users/', views.UserList.as_view(), name='users'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),

    path('posts/', views.PostList.as_view(), name = 'posts'),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name = 'post-detail'),
    path('postState/<int:post_id>/', views.post_state, name='post-state'),
    path('gamePostState/<int:post_id>/', views.game_post_state, name='game-post-state'),

    path('about/', views.about, name='about'),

    path('feed/',views.publicFeed ,name='feed'),
    path('createPost/',views.create_post_view,name='create-post'),
    path('createGamePost/',views.create_game_post_view,name='create-game-post'),
    path('deletePost/<int:post_id>/',views.delete_post_view,name='delete-post'),
    path('deleteGamePost/<int:post_id>/',views.delete_game_post_view,name='delete-game-post'),
   

    path('user/<int:user_id>/', views.user_posts, name='user_posts'),
    
    path('likePost/<int:post_id>/',views.like_post,name='like-post'),
    path('likeGamePost/<int:post_id>/',views.like_game_post,name='like-game-post'),

    path('signup/', views.signUp_view, name='signup'),
    path('login/', LoginView.as_view(
           template_name='hooptoday/loginUser.html',
           redirect_authenticated_user=True), name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('changePicture',views.change_profile_picture,name='changePicture'),

    path('favicon.ico', views.favicon_not_found),

    path('nbaLegendQuiz/',views.nba_legend_quiz,name='nba-legend-quiz'),
    path('nbaPlayerQuiz/',views.nba_player_quiz,name='nba-player-quiz'),

    path('simulateGame/',views.simulate_game,name='simulate-game'),
]


urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]

handler404 = views.error_404_view
