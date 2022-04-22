from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import apps
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import (
    UserCreationForm as DjangoUserCreationForm,
    AuthenticationForm as DjangoAuthenticationForm,
)
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import *
from django import forms

from .utils import send_email_for_verify


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


class AuthenticationForm(DjangoAuthenticationForm):

    def clean(self):   # взято из django/auth/forms class AuthenticationForm
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password,
            )
            if not self.user_cache.email_verify:
                send_email_for_verify(self.request, self.user_cache)
                raise ValidationError(
                    'Email not verify, check your email',
                    code='invalid_login',
                )

            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data


class OrderedModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def clean(self, value):
        qs = super().clean(value)
        keys = list(map(int, value))
        return sorted(qs, key=lambda v: keys.index(v.pk))


'''class ReorderProductImagesForm(forms.ModelForm):
    ordered_images = OrderedModelMultipleChoiceField(queryset=ProductImage.objects.none())

    class Meta:
        model = Ad
        fields = ()

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if self.instance:
                self.fields["ordered_images"].queryset = self.instance.images.all()

        def save(self):
            for order, image in enumerate(self.cleaned_data["ordered_images"]):
                image.sort_order = order
                image.save()
                return self.instance
'''