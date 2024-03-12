from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    owner = models.ForeignKey('auth.User', related_name='posts', on_delete=models.CASCADE)

    createdDate = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=150)
    likes = models.IntegerField(default=0)

class GamePost(models.Model):
    owner = models.ForeignKey('auth.User', related_name='game_posts', on_delete=models.CASCADE)

    createdDate = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)


    myTeamName = models.TextField(max_length=20)
    awayTeamName = models.TextField(max_length=20)

    myScore = models.IntegerField(default=0)
    awayScore = models.IntegerField(default=0)

    result = models.TextField(max_length=1, blank=False)
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image_url = models.CharField(max_length=255, blank=True, null=True)


    liked_posts = models.ManyToManyField('hooptoday.Post', blank=True)
    liked_game_posts = models.ManyToManyField('hooptoday.GamePost', blank=True)

    
    # Add additional fields as needed

    def __str__(self):
        return self.user.username
    
class Comment(models.Model):
    text = models.TextField(max_length=150)
    createdDate = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_connected = models.ForeignKey(Post, on_delete=models.CASCADE)