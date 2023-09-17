from django import forms
from water.models import WaterConsumption
from django.forms import ModelForm

from django.utils.translation import gettext as _


class WaterConsumptionForm(ModelForm):
    amount_drank = forms.FloatField(label='', widget=forms.TextInput(attrs={'placeholder': _('Amount Drank'),'class': 'form-control'}))

    class Meta:
        model = WaterConsumption
        fields = ('amount_drank',)


