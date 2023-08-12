# from django.contrib.auth import get_user_model
# from django.contrib.auth.forms import UserCreationForm
# from django import forms
#
# User = get_user_model()
#
#
# class RegisterForm(UserCreationForm):
#     email = forms.EmailField()
#
#     class Meta:
#         model = User
#         fields = ["username", "email", "password1", "password2"]
#
#
# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ("first_name", "last_name", "image", "biography")