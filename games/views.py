from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView

from games.models import Game
from games.utils import DataMixin
from users.models import UserList


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page not found 404</h1> <a href='/'>На главную страницу</a>")


def index(request):
    return render(request,  'games/index.html', {'title': 'CollGame - главная', 'user': request.user})


def terms_view(request):
    return render(request, 'terms.html', {'title': 'Пользовательское соглашение'})


class FindGames(ListView):
    model = Game
    template_name = 'games/find-result.html'
    context_object_name = 'games'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        game_name = self.request.GET.get('name', '')

        if game_name != '':
            context['title'] = f'Поиск по играм - {game_name}'
        else:
            context['title'] = 'Поиск по играм'

        return context

    def get_queryset(self):
        return Game.objects.filter(Q(name__icontains=self.request.GET.get('name', '')) & Q(is_published=True))


def game_page(request, game_slug):

    game = get_object_or_404(Game, slug=game_slug, is_published=True)

    releases = game.release_set.all()
    reviews = game.review_set.all()

    review_likes = []
    if request.user.is_authenticated:
        for review in reviews:
            liked = request.user.likereview_set.filter(review=review).exists()
            review_likes.append([review, liked])
    else:
        for review in reviews:
            review_likes.append([review, False])

    links = game.gameslinks_set.all()

    data = {'game': game, 'title': game.name, 'releases': releases, 'links': links, 'reviews': review_likes}
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

            for userList in request.user.userlist_set.all():  # Удаляем игры из списков пользователя
                userList.games.remove(game)

    return redirect('game_page', game_slug=game_slug)
