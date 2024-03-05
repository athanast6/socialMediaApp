from django.contrib import admin
from .models import Post,GamePost,UserProfile
from .forms import CustomUserCreationForm


admin.site.register(Post)
admin.site.register(GamePost)
admin.site.register(UserProfile)


