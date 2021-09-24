from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from blog.models import Profile, Comment, Post


class PostDocumentForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = Post
        fields = ('title', 'body', 'image')


class CommentForm(forms.ModelForm):
    author = forms.CharField(
        max_length=60,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Your Name"
        }),
        required=False
    )
    body = forms.CharField(widget=forms.Textarea(
        attrs={
            "class": "form-control",
            "placeholder": "Leave a comment!"
        })
    )
    image = forms.ImageField(required=False)
    following_comment_id = forms.IntegerField(required=False)

    class Meta:
        model = Comment
        exclude = ['created', 'post', 'user']


class AccountForm(forms.ModelForm):
    name = forms.CharField(help_text=' (Name)')
    surname = forms.CharField(help_text=' (Surname)')
    about_me = forms.CharField(help_text=' (About me)', required=False)

    class Meta:
        model = Profile
        fields = ('name', 'surname', 'about_me')


class ExtendedRegisterForm(UserCreationForm):
    name = forms.CharField(help_text="Имя")
    surname = forms.CharField(help_text='Фамилия')
    about_me = forms.CharField(help_text='Обо мне (Optional)', required=False)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
