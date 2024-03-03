import django.forms as forms

from activity.models import *


class AddReviewForm(forms.ModelForm):
    stars = forms.ChoiceField(label='Оценка', choices=[(str(i), str(i)) for i in range(1, 6)])
    delete = forms.BooleanField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Review
        fields = ['description', 'stars']
        labels = {
            'description': 'Комментарий',
            'stars': 'Оценка',
        }


class GameDictionaryForm(forms.ModelForm):
    class Meta:
        model = GameDictionary
        fields = ['name', 'game', 'description']


class GameDictionaryUpdateForm(forms.ModelForm):
    class Meta:
        model = GameDictionary
        fields = ['name', 'game', 'description', 'is_active']


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['description', 'hours']