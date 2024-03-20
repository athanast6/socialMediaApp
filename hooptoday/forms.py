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



class NBAGameSimulatorForm(forms.Form):
   
    teams = [
        ('UCONN', '1 - Connecticut (UConn)'),
        ('HOU', '1 - Houston'),
        ('PUR', '1 - Purdue'),
        ('NCAR', '1 - North Carolina'),
        ('TENN', '2 - Tennessee'),
        ('IOWAST', '2 - Iowa State'),
        ('MARQ', '2 - Marquette'),
        ('ARZ', '2 - Arizona'),
        ('BAYL', '3 - Baylor'),
        ('CREIGH', '3 - Creighton'),
        ('UK', '3 - Kentucky'),
        ('ILL', '3 - Illinois'),
        ('DUKE', '4 - Duke'),
        ('KAN', '4 - Kansas'),
        ('AUBRN', '4 - Auburn'),
        ('ALA', '4 - Alabama'),
        ('SDST', '5 - San Diego State'),
        ('WISC', '5 - Wisconsin'),
        ('STMRY', '5 - Saint Mary\'s (CA)'),
        ('GNZG', '5 - Gonzaga'),
        ('BYU', '6 - Brigham Young'),
        ('CLMSN', '6 - Clemson'),
        ('TXTECH', '6 - Texas Tech'),
        ('SC', '6 - South Carolina'),
        ('FL', '7 - Florida'),
        ('WASHST', '7 - Washington State'),
        ('TX', '7 - Texas'),
        ('DAY', '7 - Dayton'),
        ('NEBR', '8 - Nebraska'),
        ('UTAHST', '8 - Utah State'),
        ('FLATL', '8 - Florida Atlantic'),
        ('MSPST', '8 - Mississippi State'),
        ('MST', '9 -  Michigan State'),
        ('TXAM', '9 - Texas A&M'),
        ('TCU', '9 - TCU'),
        ('NW', '9 - Northwestern'),
        ('NEVADA', '10 - Nevada'),
        ('BOISE', '10 - Boise State'),
        ('COL', '10 - Colorado'),
        ('DRAKE', '10 - Drake'),
        ('VIR', '10 - Virginia'),
        ('COLST', '10 - Colorado State'),
        ('NMX', '11 - New Mexico'),
        ('ORE', '11 - Oregon'),
        ('NCST', '11 - North Carolina State'),
        ('DUQ', '11 - Duquesne'),
        ('GCAN', '12 - Grand Canyon'),
        ('JMAD', '12 - James Madison'),
        ('MCNST', '12 - McNeese'),
        ('UAB', '12 - UAB'),
        ('VERM', '13 - Vermont'),
        ('YALE', '13 - Yale'),
        ('SAMF', '13 - Samford'),
        ('CHAR', '13 - Charleston'),
        ('OAK', '14 - Oakland'),
        ('AKRON', '14 - Akron'),
        ('MHST', '14 - Morehead State'),
        ('COLG', '14 - Colgate'),
        ('LBST', '15 - Long Beach State'),
        ('WKENT', '15 - Western Kentucky'),
        ('SDKST', '15 - South Dakota State'),
        ('STPETE', '15 - St. Pete/s'),
        ('LONGWD', '16 - Longwood'),
        ('STETSN', '16 - Stetson'),
        ('MONST', '16 - Montana State'),
        ('GRMBST', '16 - Grambling State'),
        ('HOWRD', '16 - Howard'),
        ('WAG', '16 - Wagner')
    ]
    

    team1 = forms.ChoiceField(choices=teams)
    team2 = forms.ChoiceField(choices=teams)