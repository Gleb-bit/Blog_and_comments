from datetime import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import generic

from blog.forms import CommentForm, ExtendedRegisterForm, AccountForm, PostDocumentForm
from blog.models import Post, Comment, Profile, FollowingComment


def get_now():
    return datetime.now()


class ListPostView(generic.ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'list_post.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by('-created')
        return queryset


class CreatePostView(LoginRequiredMixin, generic.CreateView):
    model = Post
    template_name = 'create_post.html'
    form_class = PostDocumentForm

    def post(self, request, *args, **kwargs):
        blog_form = PostDocumentForm(request.POST, request.FILES)

        if blog_form.is_valid():
            title = blog_form.cleaned_data.get('title')
            body = blog_form.cleaned_data.get('body')
            profile = request.user.profile
            image = blog_form.cleaned_data.get('image')

            Post.objects.create(title=title, body=body, profile=profile, image=image)

            return HttpResponseRedirect('/blog/')

        return render(request, 'create_post.html', context={'form': blog_form})


class EditPostView(generic.UpdateView):
    model = Post
    form_class = PostDocumentForm
    template_name = 'edit_post.html'
    context_object_name = 'post'

    def get_success_url(self):
        post = self.object
        return f'/blog/{post.pk}/'


class DeletePostView(generic.DeleteView):
    model = Post
    template_name = 'delete_post_confirm.html'
    success_url = '/blog/'


class DetailPostView(generic.DetailView):

    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']

        post = Post.objects.get(pk=pk)
        comments = Comment.objects.filter(post=post)
        form = CommentForm()

        context = {
            "post": post,
            'comments': comments,
            'form': form,
        }
        return render(request, "detail_post.html", context)

    def post(self, request, pk):

        post = Post.objects.get(pk=pk)
        comments = Comment.objects.filter(post=post)
        form = CommentForm(request.POST, request.FILES)
        print(form.errors)

        if form.is_valid():
            author = self.get_author_name(request, form)

            comment = Comment(
                author=author,
                body=form.cleaned_data['body'],
                image=form.cleaned_data['image'] if 'image' in form.cleaned_data else None,
                post=post,
                user=request.user if isinstance(request.user, User) else None
            )
            comment.save()

        context = {'post': post, 'comments': comments, 'form': form}
        return render(request, "detail_post.html", context)

    def get_author_name(self, request, form):
        if request.user.is_authenticated:
            author = request.user.profile.name
        elif form.cleaned_data['author']:
            author = form.cleaned_data['author']
        else:
            author = 'Anonim'
        return author


class CreateFollowingComment(generic.CreateView):
    form_class = CommentForm
    model = Comment
    template_name = 'detail_post.html'

    def post(self, request, *args, **kwargs):
        current_post_id = request.POST['current_post_id']

        form = CommentForm(request.POST, request.FILES)

        if form.is_valid():
            parent_comment_id = request.POST['parent_comment_id']
            author = self.get_author_name(request, form)

            following_comment = FollowingComment(
                author=author,
                body=form.cleaned_data['body'],
                image=form.cleaned_data['image'] if 'image' in form.cleaned_data else None,
                user=request.user if isinstance(request.user, User) else None,
                parent_comment_id=parent_comment_id
            )
            following_comment.save()

            comment = Comment(
                author=author,
                body=form.cleaned_data['body'],
                image=form.cleaned_data['image'] if 'image' in form.cleaned_data else None,
                post_id=current_post_id,
                user=request.user if isinstance(request.user, User) else None,
                following_comment_id=parent_comment_id
            )
            comment.save()

        return redirect(f'/blog/{current_post_id}/')

    def get_author_name(self, request, form):
        if request.user.is_authenticated:
            author = request.user.profile.name
        elif form.cleaned_data['author']:
            author = form.cleaned_data['author']
        else:
            author = 'Anonim'
        return author


class EditCommentView(generic.UpdateView):
    form_class = CommentForm
    model = Comment
    template_name = 'edit_comment.html'

    def get_success_url(self):
        queryset = super().get_queryset()
        current_comment = queryset.filter(pk=self.object.pk).first()
        post = Post.objects.only('pk').filter(id=current_comment.post_id).first()

        return f'/blog/{post.pk}/'


class DeleteCommentView(generic.DeleteView):
    model = Comment
    template_name = 'delete_comment_confirm.html'

    def get_success_url(self):
        queryset = super().get_queryset()
        current_comment = queryset.filter(pk=self.object.pk).first()
        post = Post.objects.only('pk').filter(id=current_comment.post_id).first()

        return f'/blog/{post.pk}/'


class DeleteAnothersCommentView(PermissionRequiredMixin, generic.DeleteView):
    model = Comment
    success_url = '/blog/'
    template_name = 'delete_comment_confirm.html'


class DetailAccountView(generic.DetailView):
    model = Profile
    context_object_name = 'profile_list'
    template_name = 'detail_account.html'


class EditAccountView(generic.UpdateView):
    form_class = AccountForm
    model = Profile
    template_name = 'edit_account.html'

    def get_success_url(self):
        pk = self.request.user.pk
        return f'/blog/user/{pk}'


class RegisterView(generic.View):

    def get(self, request, *args, **kwargs):
        form = ExtendedRegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = ExtendedRegisterForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()

            name = form.cleaned_data.get('name')
            surname = form.cleaned_data.get('surname')
            about_me = form.cleaned_data.get('about_me')

            Profile.objects.create(user=user, name=name, surname=surname, about_me=about_me)

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            user = authenticate(username=username, password=raw_password)
            login(request, user)

            return redirect('/blog')

        form = ExtendedRegisterForm()
        return render(request, 'register.html', {'form': form})


class OurLoginView(LoginView):
    template_name = 'login.html'


class OurLogoutView(LogoutView):
    template_name = 'logout.html'
