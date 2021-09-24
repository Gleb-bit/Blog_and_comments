from datetime import datetime

from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


def comment_directory_path(instance, filename):
    now = datetime.now().strftime('%d_%m_%y-%H : %M : %S')
    return f'comment/{now}_{filename}'


def post_directory_path(instance, filename):
    now = datetime.now().strftime('%d_%m_%y-%H : %M : %S')
    return f'post/{now}_{filename}'


class Post(models.Model):
    """
    Return a post with certain fields. Profile can have multiple posts.
    """
    title = models.CharField(max_length=25)
    body = models.TextField()
    image = models.ImageField(blank=True, upload_to=post_directory_path, null=True)
    created = models.DateTimeField(auto_now=True)
    last_modified = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey('Profile', verbose_name='User',
                                on_delete=models.CASCADE,
                                related_name='posts')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Comment(models.Model):
    """
    Return a comment with certain fields. Post can have multiple comments, and so can the user
    """
    author = models.CharField(max_length=60, blank=True)
    body = models.TextField()
    image = models.ImageField(upload_to=comment_directory_path, blank=True)
    created = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, default=None, null=True, verbose_name='Пользователь', on_delete=models.CASCADE,
                             related_name='comments')
    following_comment_id = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.author

    class Meta:
        ordering = ['author']


class Profile(models.Model):
    """
    Return a profile with certain fields. One profile corresponds to one profile
    """
    user = models.OneToOneField(User, max_length=25, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    surname = models.CharField(max_length=25)
    about_me = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class FollowingComment(models.Model):
    author = models.CharField(max_length=60, blank=True)
    body = models.TextField()
    image = models.ImageField(upload_to=comment_directory_path, blank=True)
    created = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, default=None, null=True, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
