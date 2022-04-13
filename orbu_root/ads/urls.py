from django.urls import path

from ads.views import *

app_name = 'ads'

urlpatterns = [
    path('', index, name='index'),
    path('<str:page>', other_page, name='other'),
    path('accounts/login/', AdsLoginView.as_view(), name='login'),
    path('accounts/profile/', profile_view, name='profile'),
    path('accounts/logout/', logout_view, name='logout'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('registration', RegisterUser.as_view(), name='registration')
]
