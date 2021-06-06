from django import forms
from .models import Comment
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class EmailPostForm(forms.Form):
    """Форма для отправки поста на Email"""
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    """Форма для комментариев"""

    class Meta:
        model = Comment
        fields = ("name", "email", "body")


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Имя пользователя")
    password = forms.CharField(label="Пароль")


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label="Имя пользователя")
    password1 = forms.CharField(label="Пароль")
    password2 = forms.CharField(label="Подтверждение пароля")
    email = forms.EmailField(label="Email")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
