from django.contrib import admin
from .models import *



class GalleryInline(admin.TabularInline):
    model = Gallery


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    inlines = [GalleryInline, ]


admin.site.register(User)
admin.site.register(Category)








