import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from activity.forms import AddReviewForm
from activity.models import Review, LikeReview
from games.models import Game
from django.http import JsonResponse


def get_current_date():
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3)))


def update_review(saved_review, instance):

    if saved_review.description != instance.description or saved_review.stars != instance.stars:
        saved_review.created = get_current_date()

    saved_review.description = instance.description
    saved_review.stars = instance.stars

    saved_review.save()


@login_required
def add_review(request, game_slug):
    game = get_object_or_404(Game, slug=game_slug)  # Получаем игру

    # Проверяем, есть ли рецензия для текущего пользователя и игры
    try:
        saved_review = Review.objects.get(user=request.user, game=game)
    except Review.DoesNotExist:
        saved_review = None

    # Если пользователь пытается изменить рецензию
    if request.method == 'POST':
        form = AddReviewForm(request.POST)  # Получаем форму
        if form.is_valid():
            if form.cleaned_data.get('delete'):  # Если пользователь удаляет рецензию
                saved_review.delete()
            else:
                # Если рецензии уже существует
                if saved_review:
                    update_review(saved_review, form.instance)  # Обновляем рецензию
                else:
                    # Если рецензии не существует, добавляем её
                    review = form.save(commit=False)
                    review.game = game
                    review.user = request.user

                    review.created = get_current_date()
                    review.save()

            return redirect('activity:addReview', game.slug)

    # Если просто переходим на страницу, то обновляем форму
    if saved_review:
        form = AddReviewForm(instance=saved_review)
    else:
        form = AddReviewForm()

    return render(request, 'activity/add_review_page.html',
                  context={'title': 'Написание рецензии', 'game': game, 'form': form})


def like_review(request, review_id):

    review = get_object_or_404(Review, pk=review_id)
    user = request.user

    # Проверяем, не поставил ли пользователь уже лайк на эту рецензию
    like, created = LikeReview.objects.get_or_create(user=user, review=review)

    if not created:
        if like.value:
            like.delete()
            return JsonResponse({'liked': False})

    return JsonResponse({'liked': True})
