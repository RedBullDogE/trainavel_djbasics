from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import City
from .forms import CityForm


def home(request):
    if request.method == 'POST':
        form = CityForm(request.POST or None)
        if form.is_valid():
            print(form.cleaned_data)
    form = CityForm()
    cities = City.objects.all()     # pylint: disable=maybe-no-member
    return render(request, 'cities/home.html', {'objects_list': cities, 'form': form})


class CityDetailView(DetailView):
    queryset = City.objects.all()    # pylint: disable=maybe-no-member
    context_object_name = 'object'
    template_name = 'cities/detail.html'


class CityCreateView(CreateView):
    model = City
    form_class = CityForm
    template_name = 'cities/create.html'
    success_url = reverse_lazy('city:home')
