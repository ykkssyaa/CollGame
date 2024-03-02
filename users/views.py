from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView

from games.models import Game
from games.utils import DataMixin
from users.forms import RegisterUserForm
from users.models import User, UserList
from typing import Optional


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'user/login.html'
    extra_context = {'title': 'Авторизация'}


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('index'))


def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            return render(request, 'user/register_success.html', {'title': 'Успешная регистрация'})

    form = RegisterUserForm()
    return render(request, 'user/register.html', {'form': form, 'title': 'Регистрация'})


def terms(request):
    return render(request, 'terms.html')


def profile(request, username):

    user = get_object_or_404(User, username=username)
    context = {'user_p': user, 'title': f'Профиль пользователя {user.username}'}

    return render(request, 'user/profile_info.html', context)


def user_reviews(request, username):
    user = get_object_or_404(User, username=username)

    context = {'user_p': user, 'title': f'Рецензии пользователя {user.username}'}

    return render(request, 'user/profile_reviews.html', context)


class UserCollection(ListView):
    model = Game
    template_name = 'user/profile_games.html'
    context_object_name = 'games'

    def __init__(self):
        super().__init__()
        self.lst: Optional[UserList] = None
        self.user: Optional[User] = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.lst:
            context['title'] = f'Игры в списке {self.user.username} | {self.lst.name} '
        else:
            context['title'] = f'Коллекция пользователя {self.user}'

        context['user_p'] = self.user
        return context

    def get_queryset(self):
        list_id = self.request.GET.get('list', '')
        self.user = get_object_or_404(User, username=self.kwargs.get('username'))

        if list_id:
            self.lst = get_object_or_404(UserList, id=list_id)
            if self.lst.user.id == self.user.id:
                return self.lst.games.all()
            else:
                raise Http404("User list not found")
        else:
            return self.user.games.all()

