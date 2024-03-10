import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DeleteView, UpdateView

from activity.forms import AddReviewForm, GameDictionaryForm, ActivityForm, GameDictionaryUpdateForm
from activity.models import Review, LikeReview, GameDictionary, Activity
from games.models import Game
from django.http import JsonResponse, Http404


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


@login_required
def like_review(request, review_id):

    review = get_object_or_404(Review, pk=review_id)
    user = request.user

    # Проверяем, не поставил ли пользователь уже лайк на эту рецензию
    like, created = LikeReview.objects.get_or_create(user=user, review=review)

    if not created and like.value:
        like.delete()
        return JsonResponse({'liked': False})

    return JsonResponse({'liked': True})


#  ----------------------------------------------------------------

def add_game_dictionary(request):
    if request.method == 'POST':
        form = GameDictionaryForm(request.POST)
        if form.is_valid():
            dictionary = form.save(commit=False)
            dictionary.user = request.user
            dictionary.save()

            return redirect(dictionary.get_absolute_url())
    else:
        form = GameDictionaryForm()
    return render(request, 'activity/add_new_dictionary.html',
                  {'form': form, 'title': 'Добавить дневник прохождения', 'button_name': 'Добавить'})


class UpdateDictionaryView(UserPassesTestMixin, UpdateView):
    model = GameDictionary
    form_class = GameDictionaryUpdateForm
    template_name = 'activity/add_new_dictionary.html'
    extra_context = {'title': 'Изменить дневник прохождения', 'button_name': 'Обновить'}

    def get_success_url(self):
        return reverse_lazy('activity:dictionary_page', kwargs={'id': self.object.id})

    def test_func(self):
        dictionary = self.get_object()
        return self.request.user == dictionary.user


class ActivityListView(ListView):
    model = Activity
    template_name = 'activity/dictionary_activity.html'
    context_object_name = 'activities'

    def __init__(self):
        super().__init__()
        self.dictionary = None

    def get_context_data(self, **kwargs):
        context = super(ActivityListView, self).get_context_data(**kwargs)
        context['title'] = 'Дневник прохождения ' + self.dictionary.name
        context['form'] = ActivityForm()
        context['dictionary'] = self.dictionary

        return context

    def post(self, request, *args, **kwargs):
        self.dictionary = get_object_or_404(GameDictionary, pk=self.kwargs['id'])
        form = ActivityForm(request.POST)

        if form.is_valid():
            activity = form.save(commit=False)
            activity.dictionary = self.dictionary
            activity.save()

            return redirect(self.dictionary.get_absolute_url())

        return redirect(self.dictionary.get_absolute_url() + '?error=Ошибка добавления')

    def get_queryset(self):
        gamedictionary_id = self.kwargs['id']
        self.dictionary = get_object_or_404(GameDictionary, pk=gamedictionary_id, is_active=True)

        return self.dictionary.activity_set.all()


class DeleteActivityView(View):

    def post(self, request):
        activity_id = request.POST.get('id')
        if activity_id:
            try:
                activity = Activity.objects.get(pk=activity_id)
                dictionary = activity.dictionary
                activity.delete()
                return redirect(dictionary.get_absolute_url())
            except Activity.DoesNotExist:
                pass
        return Http404()


