from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Max, F
from django.urls import reverse
from mptt.managers import TreeManager
from mptt.models import MPTTModel


class SortableModel1(models.Model):
    sort_order = models.IntegerField(editable=False, db_index=True, null=True)

    class Meta:
        abstract = True

    def get_ordering_queryset(self):
        raise NotImplementedError("Unknown ordering queryset")

    def get_max_sort_order(self, qs):
        existing_max = qs.aggregate(Max("sort_order"))
        existing_max = existing_max.get("sort_order	max")
        return existing_max

    def save(self, *args, **kwargs):
        if self.pk is None:
            qs = self.get_ordering_queryset()
            existing_max = self.get_max_sort_order(qs)
            self.sort_order = 0 if existing_max is None else existing_max + 1
            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.sort_order is not None:
            qs = self.get_ordering_queryset()
            qs.filter(sort_order__gt=self.sort_order).update(
                sort_order=F("sort_order") - 1
            )
            super().delete(*args, **kwargs)


class Ad(models.Model):
    ad_title = models.CharField(max_length=300)
    ad_dt = models.DateTimeField(auto_now_add=True)
    ad_text = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, )

    class Meta:
        verbose_name = 'объявление'
        verbose_name_plural = 'объявления'

    def __str__(self):
        return self.ad_title


class ProductImages(SortableModel1):
    ad = models.ForeignKey(Ad, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="img", blank=False)
    alt = models.CharField(max_length=128, blank=True)

    class Meta:
        ordering = ("sortorder",)
        app_label = "ad"

    def get_ordering_queryset(self):
        return self.ad.images.all()


class Gallery(models.Model):
    ad_otherphoto = models.ImageField(upload_to='img/')
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='images')


class User(AbstractUser):
    send_messages = models.BooleanField(default=True, verbose_name='Уведомлять о новых комментариях?')
    is_active = models.BooleanField(default=False)
    email = models.EmailField(unique=True, )

    USERNAME_FIELD = 'email'  # unique identifier
    REQUIRED_FIELDS = ['username']  # поля,которые будут запрошены при создании пользователя с помощью  createsuperuser


class Category(MPTTModel):
    name = models.CharField(max_length=155, unique=True)
    slug = models.SlugField(max_length=155, unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    tree = TreeManager

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('ads:by_category', kwargs={'slug': self.slug})
