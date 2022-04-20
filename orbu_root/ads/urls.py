from django.urls import path
from django.views.generic import TemplateView

from ads.views import *

app_name = 'ads'

urlpatterns = [
    path('', index, name='index'),
    path('<str:page>/', other_page, name='other'),
    path('accounts/login/', AdsLoginView.as_view(), name='login'),
    path('accounts/profile/', profile_view, name='profile'),
    path('accounts/logout/', logout_view, name='logout'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('registration/', RegisterUser.as_view(), name='registration'),
    #path('confirm_email/', TemplateView.as_view(template_name='ads/confirm_email.html'), name='confirm_email'),
    #path('invalid_verify/', TemplateView.as_view(template_name='ads/invalid_verify.html'), name='confirm_email'),
    path('verify_email/<uidb64>/<token>/', EmailVerify.as_view(), name="verify_email",  # взято из django auth/urls

         ),
]
