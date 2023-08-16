from .models import Post, Comment
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'short_description', 'content', 'image', 'is_draft']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'short_description': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_draft': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class FeedbackForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender_email = forms.EmailField()
