from django.contrib.auth.models import Group, User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.http import Http404
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


class PublicFeed(TemplateView):

    template_name = 'feed.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        posts = Post.objects.all()
        game_posts = GamePost.objects.all()

        all_posts = list(posts) + list(game_posts)

        # Sort the combined list of posts by creation date
        all_posts.sort(key=lambda x: x.createdDate, reverse=True)

        posts_per_page = 10
        paginator = Paginator(all_posts, posts_per_page)
        page_number = self.request.GET.get('page', 1)

        # Get the page object for the specified page number
        page = paginator.get_page(page_number)

        #context['posts'] = all_posts
        context['page'] = page
        return context
    
def home(request):
    return render(request, 'base.html')

def signUp_view(request):
    if request.method == 'POST':
        print(request)
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():

            
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'createUser.html', {'form': form})





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
        else: return render(request, 'createPost.html')
        
    return render(request, 'createPost.html', {'form': form})


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
        else: return render(request, 'createGamePost.html')
        
    return render(request, 'createGamePost.html', {'form': form})
   
   

    
    
