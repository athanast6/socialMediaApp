# forms.py
from django import forms
from .models import Post, User, GamePost, UserProfile

from django.contrib.auth.forms import UserCreationForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field

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

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            UserProfile.objects.create(user=user)
        return user

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')  # Add other fields if needed



class ProfilePictureForm(forms.Form):
    profile_picture = forms.ImageField()


class NBAPlayerQuizForm(forms.Form):
    Age = forms.IntegerField(label='Age', initial=25)
    Three_rtg = forms.IntegerField(label='Three-point Rating', initial=70)
    Two_rtg = forms.IntegerField(label='Two-point Rating', initial=70)
    Free_throw_rtg = forms.IntegerField(label='Free Throw Rating', initial=70)
    Pass_rtg = forms.IntegerField(label='Passing Rating', initial=70)
    draw_foul_rtg = forms.IntegerField(label='Draw Foul Rating', initial=70)
    take_three_prob = forms.IntegerField(label='Take Three Probability', initial=50)
    take_two_prob = forms.IntegerField(label='Take Two Probability', initial=50)
    make_ast_prob = forms.IntegerField(label='Make Assist Probability', initial=50)
    turnover_prob = forms.IntegerField(label='Turnover Probability', initial=50)
    stamina = forms.IntegerField(label='Stamina', initial=70)
    usageRate = forms.IntegerField(label='Usage Rate', initial=70)
    rebound_rtg = forms.IntegerField(label='Rebound Rating', initial=70)
    steal_rtg = forms.IntegerField(label='Steal Rating', initial=70)
    block_rtg = forms.IntegerField(label='Block Rating', initial=70)
    height = forms.IntegerField(label='Height', initial=72)