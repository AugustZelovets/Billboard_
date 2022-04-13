from django.contrib.auth.forms import UserCreationForm

from .models import User
from django import forms


class ChangeUserInfo(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес эдектронной почты')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'send_messages')


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput())
    email = forms.EmailField(label='Email', widget=forms.EmailInput())
    first_name = forms.CharField(required=False, label='Имя', widget=forms.TextInput())
    last_name = forms.CharField(required=False, label='Фамилия', widget=forms.TextInput())
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')  # определяем порядок
