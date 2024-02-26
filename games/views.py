from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

from games.models import Game


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page not found 404</h1> <a href='/'>На главную страницу</a>")


def index(request):
    return render(request,  'games/index.html', {'title': 'CollGame - главная'})


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
    data = {'game': game, 'title': game.name}

    return render(request, 'games/game-page.html', data)
