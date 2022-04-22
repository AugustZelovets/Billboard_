from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import *


class GalleryInline(admin.TabularInline):
    model = Gallery


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    inlines = [GalleryInline, ]


class CategoryAdmin(MPTTModelAdmin):
    list_display = 'name', 'slug', 'parent',

    prepopulated_fields = {'slug': ('name',)}


admin.site.register(User)
admin.site.register(Category, CategoryAdmin,)# MPTTModelAdmin) ветвление в админке


