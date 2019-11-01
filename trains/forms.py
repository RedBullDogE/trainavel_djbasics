from django import forms
from .models import Train
from cities.models import City


class TrainForm(forms.ModelForm):
    name = forms.CharField(label='Поезд',
                           widget=forms.TextInput(
                               attrs={'class': 'form-control',
                                      'placeholder': 'Введите название поезда'}))

    from_city = forms.ModelChoiceField(label='Откуда',
                                       queryset=City.objects.all(),  # pylint: disable=maybe-no-member
                                       widget=forms.Select(
                                           attrs={'class': 'form-control',
                                                  'placeholder': 'Откуда'}))
    to_city = forms.ModelChoiceField(label='Куда',
                                     queryset=City.objects.all(),  # pylint: disable=maybe-no-member
                                     widget=forms.Select(
                                           attrs={'class': 'form-control',
                                                  'placeholder': 'Куда'}))

    travel_time = forms.CharField(label='Время в пути',
                                  widget=forms.NumberInput(
                                      attrs={'class': 'form-control',
                                             'placeholder': 'Время в пути'}))

    class Meta(object):
        model = Train
        fields = ['name', 'from_city', 'to_city', 'travel_time']
