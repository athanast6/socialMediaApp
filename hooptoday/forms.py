# forms.py
from django import forms
from .models import Post, User, GamePost, UserProfile

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


class NBALegendQuizForm(forms.Form):
    Age = forms.IntegerField(label='Age')
    Three_rtg = forms.IntegerField(label='Three-point Rating')
    Two_rtg = forms.IntegerField(label='Two-point Rating')
    Free_throw_rtg = forms.IntegerField(label='Free Throw Rating')
    Pass_rtg = forms.IntegerField(label='Passing Rating')
    draw_foul_rtg = forms.IntegerField(label='Draw Foul Rating')
    take_three_prob = forms.IntegerField(label='Take Three Probability')
    take_two_prob = forms.IntegerField(label='Take Two Probability')
    make_ast_prob = forms.IntegerField(label='Make Assist Probability')
    turnover_prob = forms.IntegerField(label='Turnover Probability')
    stamina = forms.IntegerField(label='Stamina')
    usageRate = forms.IntegerField(label='Usage Rate')
    rebound_rtg = forms.IntegerField(label='Rebound Rating')
    steal_rtg = forms.IntegerField(label='Steal Rating')
    block_rtg = forms.IntegerField(label='Block Rating')
    height = forms.IntegerField(label='Height')