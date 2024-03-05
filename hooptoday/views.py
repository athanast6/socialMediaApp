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


from .models import Post, GamePost, UserProfile
from .serializers import PostSerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly


from .forms import CreatePost, CreateGamePost, CustomUserCreationForm, ProfilePictureForm

from .cloudstorage import get_blob_service_client_account_key,upload_blob_file






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

            return redirect('about')
        

    


    
    
def about(request):
    return render(request, 'hooptoday/about.html')

def signUp_view(request):
    if request.method == 'POST':

        form = CustomUserCreationForm(request.POST)

        if form.is_valid():

            form.save()

            print(form.cleaned_data['username'])

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


def change_profile_picture(request):      
    
    #Change profile picture
    if(request.method == "POST"):

        form = ProfilePictureForm(request.POST, request.FILES)
            
        user = request.user
        username = user.username
        uploaded_image = request.FILES['profile_picture']

        image_name = uploaded_image.name
        file_ext = image_name.split('.')[-1]

        print(uploaded_image)
        
        # Rename the uploaded file to the username
        file_name = f"{username}_profile_picture.{file_ext}"

        print(file_name)
        
        # Upload the file to Azure Storage
        #blob_service_client = BlobServiceClient.from_connection_string('your_connection_string')
        container_name = 'hoop-today-blob'
        #container_client = blob_service_client.get_container_client(container_name)
        #blob_client = container_client.get_blob_client(file_name)

        blob_service_client = get_blob_service_client_account_key()

        print(blob_service_client.account_name)
        
        upload_blob_file(blob_service_client=blob_service_client,file=uploaded_image,filename=file_name,container_name=container_name)

        print(container_name)
            
        # Save the URL to the user's profile
        profile_image_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{file_name}"
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user_profile.profile_image_url = profile_image_url
        user_profile.save()

        return redirect('about')
    
    #Show profile picture form
    else:

        if(request.user.is_authenticated):
            form = ProfilePictureForm()
            return render(request, 'hooptoday/editProfile.html', {'form': form})
        
        else:
            return redirect('about')




#PROFILE
def user_posts(request, user_id):

    #Changing profile information

    

    if request.method == 'POST':
        if request.user.user_id == user_id:
            form = ProfilePictureForm()
            if form.is_valid():
                form.save()
                return redirect('profile')  # Redirect to the profile page after successful update
    else:
        form = ProfilePictureForm()

        user = User.objects.get(id=user_id)

        user_profile = UserProfile.objects.get(user=user)

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
                'form':form,
                'page':page,
                'user_id':user_id,
                'username':user.username,
                'userwins':userwins,
                'userlosses':userlosses,
                'usergames':usergames,
                'avg_points':avg_points,
                'away_avg_points':away_avg_points,
                'user_profile':user_profile,
            }

            return render(request,'hooptoday/profile.html', context=context)
        else:
            return render(request,'hooptoday/profile.html',{'username':user.username,'user_id':user_id,'form':form,'user_profile':user_profile,})



def favicon_not_found(request):
    return HttpResponseNotFound()
   
   

    
    
