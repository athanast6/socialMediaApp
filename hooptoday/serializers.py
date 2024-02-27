from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Post


class UserSerializer(serializers.HyperlinkedModelSerializer):

    posts = serializers.HyperlinkedRelatedField(many=True, view_name='post-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url','id','username','email','posts']
        

class PostSerializer(serializers.HyperlinkedModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Post
        fields = ['url','id','owner','text','likes','createdDate']