from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth import get_user_model
from .models import User, UserList


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(label="Username", widget=forms.TextInput())
    password = forms.CharField(label="Password", widget=forms.PasswordInput())
    confirm_password = forms.CharField(label="Confirm password", widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ['username', 'password', 'confirm_password', 'email', 'first_name', 'last_name']
        labels = {
            'username': 'Логин',
            'password': '<PASSWORD>',
            'confirm_password': '<PASSWORD>',
            'email': 'Email',
            'first_name': 'Имя',
            'last_name': 'Фамилия'
        }

    def clean_confirm_password(self):
        cd = self.cleaned_data
        if cd['password'] != cd['confirm_password']:
            raise forms.ValidationError('Пароли не совпадают')

        return cd['confirm_password']

    def clean_email(self):
        cd = self.cleaned_data
        if cd['email'] and get_user_model().objects.filter(email=cd['email']).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует')

        return cd['email']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['photo']


class UserListForm(forms.ModelForm):
    class Meta:
        model = UserList
        fields = ['name']
        labels = {
            'name': 'Название'
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['photo', 'first_name', 'last_name', 'bio', 'email', 'steam_id']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['photo'].required = False
        self.fields['steam_id'].required = False
        self.fields['bio'].required = False
