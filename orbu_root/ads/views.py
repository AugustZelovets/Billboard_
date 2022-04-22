from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.urls import reverse, reverse_lazy
from django.contrib.auth import logout, login
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.auth.tokens import default_token_generator as \
    token_generator
from django import forms
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from .forms import *
from .models import Ad, Gallery, User, Category
from .utils import send_email_for_verify


def index(request):
    """returns objects to home page"""
    objects_list = Ad.objects.all()
    categories_list = Category.objects.all()
    context = {
        'objects_list': objects_list,
        'categories_list': categories_list,

    }
    return render(request, 'ads/index.html', context)


def other_page(request, page):
    """ для отображения страниц, в шаблоны которых не передаются данные, имя шаблона = url  """
    try:
        template = get_template('ads/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


class AdsLoginView(LoginView):
    template_name = 'ads/login.html'
    success_url = reverse_lazy('index')


@login_required
def logout_view(request):
    logout(request)
    return redirect('ads:index')


def profile_view(request):
    return render(request, 'ads/profile.html')


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = User
    form_class = ChangeUserInfo
    template_name = 'ads/change_user_info.html'
    success_url = reverse_lazy('ads:profile')
    success_message = 'Личные данные изменены'

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    model = User
    template_name = 'ads/registration.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        send_email_for_verify(self.request, user)
        return redirect('ads:confirm_email')


class EmailVerify(View):

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            user.is_active = True
            return redirect('ads:index')

        return redirect('ads:invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,
                User.DoesNotExist, ValidationError):
            user = None
        return user


class MyLoginView(LoginView):
    form_class = AuthenticationForm


def by_category(request, slug):
    pass


'''@require_POST
@staff_member_required
def ajax_reorder_product_images(request, ad_id):
    product = get_object_or_404(Ad, pk=ad_id)
    #form = ReorderProductImagesForm(request.POST, instance=product)  # ???????
    status = 200
    ctx = {}
    if form.is_valid():
        form.save()
    elif form.errors:
        status = 400
        ctx = {"error": form.errors}
    return JsonResponse(ctx, status=status)'''









