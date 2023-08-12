from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('posts', views.posts, name='post_list'),
    path('login', views.login, name='login'),
    path('registration', views.registration, name='registration'),
]
