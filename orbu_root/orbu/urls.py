from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.views import serve
from django.urls import path, include
from django.views.decorators.cache import never_cache

from orbu import settings
from orbu.settings import MEDIA_ROOT

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('ads.urls', namespace='')),

              ] + static(settings.MEDIA_URL, document_root=MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns.append(path('static/<path:path>', never_cache(serve)))
