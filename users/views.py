import datetime
import json

from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView

from activity.views import get_current_date
from games.models import Game
from games.utils import DataMixin
from users.forms import RegisterUserForm, UserListForm
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
    context = {'user_p': user, 'title': f'Профиль пользователя {user.username}', 'add_list_form': UserListForm()}

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


def reverse_lazy_lazy(username):
    return reverse_lazy('users:profile', kwargs={'username': username})


def add_list(request):
    error_message = None
    if request.method == 'POST':
        form = UserListForm(request.POST)
        form.instance.user = request.user
        if form.is_valid():
            list_instance = form.save(commit=False)

            list_instance.created = get_current_date()
            list_instance.save()

        else:
            error_message = 'Такой список уже существует'

    return redirect(reverse_lazy_lazy(request.user.username) +
                    (f'?error={error_message}'if error_message else ''))


def delete_list(request):
    if request.method == 'POST':
        list_id = request.POST.get('list_id')
        try:
            list_to_delete = UserList.objects.get(id=list_id)
            list_to_delete.delete()

        except UserList.DoesNotExist:
            return redirect(reverse_lazy_lazy(request.user.username) + '?error=Ошибка удаления списка')

    return redirect(reverse_lazy_lazy(request.user.username))


def add_game_to_list(request):
    if request.method == 'POST':
        # Читаем данные из тела запроса JSON
        data = json.loads(request.body.decode('utf-8'))

        # Получаем идентификатор списка и игры из данных запроса
        list_id = data.get('list_id')
        game_id = data.get('game_id')

        # Получаем объекты списка пользователя и игры
        user_list = get_object_or_404(UserList, pk=list_id)
        game = get_object_or_404(Game, pk=game_id)

        # Проверяем, не добавлена ли игра уже в список пользователя
        if game in user_list.games.all():
            # Если игра уже в списке, удаляем ее из списка
            user_list.games.remove(game)
            return JsonResponse({'status': 'success', 'message': 'Игра успешно удалена из списка', 'action': 'deleted'}, status=200)
        else:
            # Если игра не в списке, добавляем ее в список
            user_list.games.add(game)
            return JsonResponse({'status': 'success', 'message': 'Игра успешно добавлена в список', 'action': 'added'}, status=200)

    return JsonResponse({'status': 'error', 'message': 'Недопустимый запрос'}, status=400)


def lists_with_game(request):
    if request.method == 'GET' and 'game_id' in request.GET:
        game_id = request.GET.get('game_id')

        try:
            game = Game.objects.get(pk=game_id)
        except Game.DoesNotExist:
            return JsonResponse({'error': 'Игра с указанным ID не найдена'}, status=404)

        list_with_game = UserList.objects.filter(games=game)
        lists_data = [{'id': user_list.id, 'name': user_list.name} for user_list in list_with_game]

        return JsonResponse(lists_data, safe=False)

    return JsonResponse({'error': 'Недопустимый запрос'}, status=400)
