from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Post, Comment, Profile


class UserSerializer(serializers.HyperlinkedModelSerializer):
    comments = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='comments-detail')

    class Meta:
        model = User
        fields = ['id', 'username', 'last_login', 'is_staff', 'is_superuser', 'is_active', 'comments']


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    posts = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='posts-detail')
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['id', 'name', 'surname', 'about_me', 'posts', 'user']


class PostSerializer(serializers.HyperlinkedModelSerializer):
    profile = serializers.ReadOnlyField(source='profile.name')
    comments = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='comments-detail')

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'image', 'profile', 'comments']

    # def create(self, validated_data):  # метод для сохранения объекта поста
    #     instance = Post.objects.create(title=validated_data['title'], body=validated_data['body'],
    #                                    image=validated_data['image'],
    #                                    profile=validated_data['profile'])
    #
    #     return instance
    #
    # def update(self, instance, validated_data):  # метод для обновления объекта поста
    #     for key, value in validated_data.items():  # цикл для обновления данных объекта поста
    #         setattr(instance, key, value)
    #
    #     instance.save(update_fields=['title', 'body', 'image', 'profile'])
    #
    #     return instance


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    post = serializers.ReadOnlyField(source='post.title')
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ['id', 'author', 'body', 'image', 'post', 'user', 'following_comment_id']

    def to_representation(self, instance):
        self._instanse = instance
        return super(CommentSerializer, self).to_representation(instance)
