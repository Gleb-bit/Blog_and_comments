from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, mixins

from .models import Post, Comment, Profile
from .permissions import IsPostOwnerOrReadOnly, IsUserOwnerOrReadOnly, IsProfileOwnerOrReadOnly, \
    IsCommentOwnerOrReadOnly
from .serializers import PostSerializer, CommentSerializer, ProfileSerializer, UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    '''Information about post'''
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsPostOwnerOrReadOnly]


class CommentViewSet(viewsets.ModelViewSet):
    '''Information about comments'''
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsCommentOwnerOrReadOnly]


class ProfileViewSet(viewsets.ModelViewSet):
    '''Information about profile'''
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsProfileOwnerOrReadOnly]


class UserViewSet(viewsets.ModelViewSet):
    '''Information about user'''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsUserOwnerOrReadOnly]
