import datetime
import json

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, RedirectView

from activity.views import get_current_date
from games.models import Game
from games.utils import DataMixin
from users.forms import RegisterUserForm, UserListForm, UserUpdateForm
from users.models import User, UserList
from typing import Optional


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'user/login.html'
    extra_context = {'title': 'Авторизация'}


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('index'))


DEFAULT_LIST_NAME = ['Список желаемого', 'Пройденные', 'Играю']


def create_default_lists(user: User):

    today = get_current_date()

    for name in DEFAULT_LIST_NAME:
        user_list = UserList()
        user_list.name = name
        user_list.user = user
        user_list.created = today

        user_list.save()


def register(request):
    form = RegisterUserForm()

    if request.method == 'POST':
        form = RegisterUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            create_default_lists(user)

            return render(request, 'user/register_success.html', {'title': 'Успешная регистрация'})

    if request.user.is_authenticated:
        return redirect(reverse_lazy_lazy(request.user.get_username()))

    return render(request, 'user/register.html', {'form': form, 'title': 'Регистрация'})


def terms(request):
    return render(request, 'terms.html')


def profile(request, username):
    user = get_object_or_404(User, username=username)
    if user == request.user:
        dictionaries = user.gamedictionary_set.all()
    else:
        dictionaries = user.gamedictionary_set.filter(is_active=True)

    context = {'user_p': user,
               'title': f'Профиль пользователя {user.username}',
               'add_list_form': UserListForm(),
               'dicts': dictionaries}

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


class UpdateUserPage(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'user/profile_update.html'
    extra_context = {'title': 'Изменение профиля'}

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'username': self.request.user.username})


class DeleteAccountView(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('index')

    def get_redirect_url(self, *args, **kwargs):
        # Удаление аккаунта пользователя
        self.request.user.delete()
        # Выход пользователя из системы после удаления аккаунта
        logout(self.request)
        return super().get_redirect_url(*args, **kwargs)

#  ----------------------------------------------------------------
#  Работа со списками

def reverse_lazy_lazy(username):
    return reverse_lazy('users:profile', kwargs={'username': username})


@login_required
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


@login_required
def delete_list(request):
    if request.method == 'POST':
        list_id = request.POST.get('list_id')
        try:
            list_to_delete = UserList.objects.get(id=list_id)
            list_to_delete.delete()

        except UserList.DoesNotExist:
            return redirect(reverse_lazy_lazy(request.user.username) + '?error=Ошибка удаления списка')

    return redirect(reverse_lazy_lazy(request.user.username))


@login_required
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
            if game not in request.user.games.all():  # Если игры нет в коллекции пользователя
                request.user.games.add(game)

            user_list.games.add(game)
            return JsonResponse({'status': 'success', 'message': 'Игра успешно добавлена в список', 'action': 'added'}, status=200)

    return JsonResponse({'status': 'error', 'message': 'Недопустимый запрос'}, status=400)


@login_required
def delete_game_from_list(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        game_id = data.get('game_id')
        list_id = data.get('list_id')

        game = get_object_or_404(Game, id=game_id)

        if list_id:
            user_list = get_object_or_404(UserList, id=list_id)

            if user_list.user.pk != request.user.pk:
                return JsonResponse({'success': False, 'error': 'Нет доступа к списку'})

            if game in user_list.games.all():
                user_list.games.remove(game_id)
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Игра не найдена в списке пользователя'})
        else:
            if game in request.user.games.all():
                request.user.games.remove(game)
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Игра не найдена в коллекции пользователя'})

    # Возвращаем ошибку метода запроса, если это не POST запрос
    return JsonResponse({'success': False, 'error': 'Метод запроса должен быть POST'})


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
