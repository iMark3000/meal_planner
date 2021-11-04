import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class PlannedRecipeEventForm(forms.Form):
    date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    # Read this: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms

    def cleaned_date(self):
        data = self.cleaned_data['date']

        if data < datetime.date.today():
            raise ValidationError(_('Cannot choose a date in the past'))

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('You are choosing a date more than a month in the future'))

        return data