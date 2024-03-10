from io import BytesIO

from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile

from .models import User, UserList
from PIL import Image


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
        fields = ['username', 'password', 'confirm_password', 'email', 'first_name']
        labels = {
            'username': 'Логин',
            'password': '<PASSWORD>',
            'confirm_password': '<PASSWORD>',
            'email': 'Email',
            'first_name': 'Имя',
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

    def save(self, commit=True):
        user = super(UserUpdateForm, self).save(commit=False)

        # Если загружено изображение
        if 'photo' in self.cleaned_data:
            photo = self.cleaned_data['photo']
            if photo:
                # Открываем изображение с помощью PIL
                img = Image.open(photo)

                # Определяем размеры центральной части изображения
                width, height = img.size
                min_dim = min(width, height)
                left = int((width - min_dim) / 2)
                top = int((height - min_dim) / 2)
                right = int((width + min_dim) / 2)
                bottom = int((height + min_dim) / 2)

                # Обрезаем изображение, оставляя центральную часть
                img_cropped = img.crop((left, top, right, bottom))

                # Перезаписываем изображение
                img_cropped_io = BytesIO()
                img_cropped.save(img_cropped_io, format='JPEG')

                user.photo.save(photo.name, ContentFile(img_cropped_io.getvalue()), save=False)

            if commit:
                user.save()
            return user
