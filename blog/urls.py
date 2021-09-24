from django.urls import path

from .views import *

urlpatterns = [
    path('', ListPostView.as_view(), name="list_post"),
    path('<int:pk>/', DetailPostView.as_view(), name="detail_post"),
    path('create/post', CreatePostView.as_view(), name='create_post'),
    path('edit/comment/<int:pk>/', EditCommentView.as_view(), name='edit_comment'),
    path('edit/post/<int:pk>/', EditPostView.as_view(), name='edit_post'),
    path('delete/comment/<int:pk>/', DeleteCommentView.as_view(), name='del_comment'),
    path('create/folowing_comment/', CreateFollowingComment.as_view(), name='create_follow_com'),
    path('delete/post/<int:pk>/', DeletePostView.as_view(), name='del_post'),
    path('user/register/', RegisterView.as_view(), name='register'),
    path('user/login/', OurLoginView.as_view(), name='login'),
    path('user/logout/', OurLogoutView.as_view(), name='logout'),
    path('user/<int:pk>', DetailAccountView.as_view(), name='detail_account'),
    path('user/<int:pk>/edit', EditAccountView.as_view(), name='edit_account'),

]
