# forms.py
from django import forms
from .models import Post, User, GamePost

from django.contrib.auth.forms import UserCreationForm

class CreatePost(forms.Form):
    text = forms.CharField(max_length=100)

    class Meta:
        model = Post
        fields = ['text']


class CreateGamePost(forms.Form):
    myTeamName = forms.CharField(max_length=20)
    awayTeamName = forms.CharField(max_length=20)
    myScore = forms.IntegerField()
    awayScore = forms.IntegerField()


    OPTIONS = [
        ('W', 'W'),
        ('D', 'D'),
        ('L', 'L'),
    ]
    result = forms.ChoiceField(choices=OPTIONS)

    class Meta:
        model = GamePost
        fields = ['myTeamName','awayTeamName','myScore','awayScore','result']



class CustomUserCreationForm(UserCreationForm):
    

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')  # Add other fields if needed
