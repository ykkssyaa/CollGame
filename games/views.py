from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect

from games.models import Game
from users.models import User


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page not found 404</h1> <a href='/'>На главную страницу</a>")


def index(request):
    return render(request,  'games/index.html', {'title': 'CollGame - главная', 'user': request.user})


def terms_view(request):
    return render(request, 'terms.html', {'title': 'Пользовательское соглашение'})


def find_games(request):

    game_name = request.GET.get('name', '')

    if game_name != '':
        games = Game.objects.filter(name__icontains=game_name)
        title = f'Поиск по играм - {game_name}'
    else:
        games = Game.objects.all()
        title = f'Поиск по играм'

    data = {'game_name': game_name, 'games': games, 'title': title}
    return render(request, 'games/find-result.html', data)


def game_page(request, game_slug):

    game = Game.objects.get(slug=game_slug)

    releases = game.release_set.all()
    links = game.gameslinks_set.all()

    data = {'game': game, 'title': game.name, 'releases': releases, 'links': links}
    return render(request, 'games/game-page.html', data)


@login_required
def add_game(request, game_slug):
    if request.method == 'POST':
        if request.user.is_authenticated:
            game = Game.objects.get(slug=game_slug)
            request.user.games.add(game)

    return redirect('game_page', game_slug=game_slug)


@login_required
def delete_game(request, game_slug):
    if request.method == 'POST':
        if request.user.is_authenticated:
            game = Game.objects.get(slug=game_slug)
            request.user.games.remove(game)

    return redirect('game_page', game_slug=game_slug)
