from .models import User
from django import forms


class ChangeUserInfo(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес эдектронной почты')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'send_messages')