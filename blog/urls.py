from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth.views import LoginView, LogoutView

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('create_post/', views.CreatePostView.as_view(), name='create_post'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='update_post'),
    path('user_posts/', views.UserPostListView.as_view(), name='user_post_list'),

    path('post/<int:pk>/comments/', views.CommentListView.as_view(), name='post_comments'),
    path('comment/create/<int:post_id>/', views.CommentCreateView.as_view(), name='create_comment'),

    path('feedback/', views.FeedbackView.as_view(), name='feedback'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path("profile/", views.UserDetailView.as_view(), name="profile"),
    path('user/<int:pk>/', views.UserProfileView.as_view(), name='user_profile'),
    path("registration/", views.RegisterFormView.as_view(), name="registration"),
    path("update_profile/", views.UserUpdateView.as_view(), name="update_profile"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
