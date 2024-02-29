from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy

from users.forms import RegisterUserForm
from users.models import User


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

            return render(request, 'user/register_success.html',)

    form = RegisterUserForm()
    return render(request, 'user/register.html', {'form': form})


def terms(request):
    return render(request, 'terms.html')


def profile(request, username):

    user = get_object_or_404(User, username=username)

    return render(request, 'user/profile_info.html', {'user_p': user})


def user_reviews(request, username):
    user = get_object_or_404(User, username=username)

    return render(request, 'user/profile_reviews.html', {'user_p': user})


def user_collection(request, username):
    user = get_object_or_404(User, username=username)

    return render(request, 'user/profile_games.html', {'user_p': user})
