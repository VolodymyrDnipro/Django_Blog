from django.shortcuts import render


def index(request):
    return render(request, 'blog/index.html')


def posts(request):
    return render(request, 'blog/post_list.html')



def login(request):
    return render(request, 'registration/login.html')


def registration(request):
    return render(request, 'registration/registration.html')

