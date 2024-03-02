import django.forms as forms

from activity import models


class AddReviewForm(forms.ModelForm):
    stars = forms.ChoiceField(label='Оценка', choices=[(str(i), str(i)) for i in range(1, 6)])
    delete = forms.BooleanField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = models.Review
        fields = ['description', 'stars']
        labels = {
            'description': 'Комментарий',
            'stars': 'Оценка',
        }

