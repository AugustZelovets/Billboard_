from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.urls import reverse, reverse_lazy
from django.contrib.auth import logout, login
from django.views.generic.edit import UpdateView, CreateView

from .forms import ChangeUserInfo, RegisterUserForm
from .models import Ad, Gallery, User


def index(request):
    objects_list = Ad.objects.all()
    context = {
        'objects_list': objects_list,
    }
    return render(request, 'ads/index.html', context)


def other_page(request, page):
    """ Выводит страницы без подгрузки данных в них из БД (about)"""
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
    form_class = UserCreationForm
    #model = User
    template_name = 'ads/registration.html'
    success_url = reverse_lazy('login')
    fields = ['username', 'first_name']


    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')





'''
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))'''









