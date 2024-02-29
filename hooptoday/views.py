from django.contrib.auth.models import Group, User
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.http import Http404, HttpResponseForbidden, HttpResponseNotFound, HttpResponse
from django.views.generic import TemplateView, CreateView
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, viewsets, generics, renderers
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.renderers import TemplateHTMLRenderer


from .models import Post, GamePost
from .serializers import PostSerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly


from .forms import CreatePost, CreateGamePost, CustomUserCreationForm






def error_404_view(request, exception):
   
    # we add the path to the 404.html file
    # here. The name of our HTML file is 404.html
    return render(request, 'hooptoday/404.html')

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('users', request=request, format=format),
        'posts': reverse('posts', request=request, format=format)
    })


class UserList(generics.ListAPIView):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostList(generics.ListCreateAPIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self,serializer):
        serializer.save(owner=self.request.user)
    


class PostDetail(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    queryset = Post.objects.all()
    serializer_class = PostSerializer

def publicFeed(request):


    if(request.method == "GET"):

        print(request)

        queryset = Post.objects.all()

        if queryset.exists():
            posts = Post.objects.all()
            game_posts = GamePost.objects.all()
            

            all_posts = list(posts) + list(game_posts)

            # Sort the combined list of posts by creation date
            all_posts.sort(key=lambda x: x.createdDate, reverse=True)

            posts_per_page = 10
            paginator = Paginator(all_posts, posts_per_page)
            page_number = request.GET.get('page', 1)

            # Get the page object for the specified page number
            page = paginator.get_page(page_number)

            #context['posts'] = all_posts
            context = {
                'page':page
            }

            return render(request, 'hooptoday/feed.html', context)
        
        else:

            return redirect('home')
        

    


    
    
def home(request):
    return render(request, 'hooptoday/base.html')

def signUp_view(request):
    if request.method == 'POST':
        print(request)
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():

            
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'hooptoday/createUser.html', {'form': form})





def logout_view(request):
    logout(request)
    # Redirect to a desired URL after logout (e.g., home page)
    return redirect('login')



def create_post_view(request):

    print(request)
    if request.method == 'POST':

        

        form = CreatePost(request.POST)
        if form.is_valid():
            # Process form data
            #name = form.cleaned_data['name']
            
            
            # Do something with the data, like saving to a database
            # Redirect to a success page or do something else

            newPost = Post(owner = request.user,
                           text = form.cleaned_data['text'],
                           likes =0)
            
            newPost.save()


            return redirect('feed')
    else:
        
        if(request.user.is_authenticated):form = CreatePost()
        else: return render(request, 'hooptoday/createPost.html')
        
    return render(request, 'hooptoday/createPost.html', {'form': form})


def create_game_post_view(request):
    if request.method == 'POST':

        

        form = CreateGamePost(request.POST)
        if form.is_valid():
            # Process form data

            newPost = GamePost(
            
            owner = request.user,
            myTeamName = form.cleaned_data['myTeamName'],
            awayTeamName = form.cleaned_data['awayTeamName'],
            myScore = form.cleaned_data['myScore'],
            awayScore = form.cleaned_data['awayScore'],
            result = form.cleaned_data['result'],
            likes = 0
            )
           
        
            # Do something with the data, like saving to a database
            # Redirect to a success page or do something else
            newPost.save()


            return redirect('feed')
    else:
        
        if(request.user.is_authenticated):form = CreateGamePost()
        else: return render(request, 'hooptoday/createGamePost.html')
        
    return render(request, 'hooptoday/createGamePost.html', {'form': form})

def delete_post_view(request,post_id):

    post = get_object_or_404(Post, pk=post_id)
    
    post.delete()

    return redirect('feed')

def delete_game_post_view(request,post_id):

    game_post = get_object_or_404(GamePost, pk=post_id)
    
    game_post.delete()

    return redirect('feed')


#PROFILE
def user_posts(request, user_id):

    user = User.objects.get(id=user_id)

    posts = Post.objects.filter(owner_id=user_id)
    game_posts = GamePost.objects.filter(owner_id=user_id)
    if posts.exists() | game_posts.exists():

        
        userwins=0
        userlosses=0
        usergames = 0
        totalpoints=0
        otherpoints=0
        avg_points=0
        away_avg_points=0

        if game_posts.exists():
            for game in game_posts:
                if game.result == "W":
                    userwins+=1
                else:
                    userlosses+=1
                usergames +=1
                totalpoints+=game.myScore
                otherpoints+=game.awayScore

        if usergames != 0:
            avg_points=totalpoints/usergames
            away_avg_points=otherpoints/usergames
            
        all_posts = list(posts) + list(game_posts)

        # Sort the combined list of posts by creation date
        all_posts.sort(key=lambda x: x.createdDate, reverse=True)

        posts_per_page = 10
        paginator = Paginator(all_posts, posts_per_page)
        page_number = request.GET.get('page', 1)

        # Get the page object for the specified page number
        page = paginator.get_page(page_number)

    
        context = {
            'page':page,
            'username':user.username,
            'userwins':userwins,
            'userlosses':userlosses,
            'usergames':usergames,
            'avg_points':avg_points,
            'away_avg_points':away_avg_points,
        }

        return render(request,'hooptoday/profile.html', context=context)
    else:
        return render(request,'hooptoday/profile.html',{'username':user.username})



def favicon_not_found(request):
    return HttpResponseNotFound()
   
   

    
    
