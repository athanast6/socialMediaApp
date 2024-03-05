from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    owner = models.ForeignKey('auth.User', related_name='posts', on_delete=models.CASCADE)

    createdDate = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    likes = models.IntegerField()

class GamePost(models.Model):
    owner = models.ForeignKey('auth.User', related_name='game_posts', on_delete=models.CASCADE)

    createdDate = models.DateTimeField(auto_now_add=True)

    myTeamName = models.TextField(max_length=20)
    awayTeamName = models.TextField(max_length=20)

    myScore = models.IntegerField(default=0)
    awayScore = models.IntegerField(default=0)

    result = models.TextField(max_length=1, blank=False)

    likes = models.IntegerField()

    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image_url = models.CharField(max_length=255, blank=True, null=True)

    
    # Add additional fields as needed

    def __str__(self):
        return self.user.username
