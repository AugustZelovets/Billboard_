from django.contrib.auth.models import AbstractUser
from django.db import models


class Ad(models.Model):
    ad_mainphoto = models.ImageField(upload_to='img/')
    ad_title = models.CharField(max_length=300)
    ad_dt = models.DateTimeField(auto_now_add=True)
    ad_text = models.TextField()

    def __str__(self):
        return self.ad_title

    class Meta:
        verbose_name = 'объявление'
        verbose_name_plural = 'объявления'


class Gallery(models.Model):
    ad_otherphoto = models.ImageField(upload_to='img/')
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='images')


class User(AbstractUser):
    send_messages = models.BooleanField(default=True, verbose_name='Уведомлять о новых комментариях?')
    is_active = models.BooleanField(default=False)
    email = models.EmailField(unique=True,)

    USERNAME_FIELD = 'email'  # unique identifier
    REQUIRED_FIELDS = ['username']  # поля,которые будут запрошены при создании пользователя с помощью  createsuperuser
