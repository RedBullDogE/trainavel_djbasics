from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Train
from .forms import TrainForm


def home(request):
    train_list = Train.objects.all()     # pylint: disable=maybe-no-member
    paginator = Paginator(train_list, 8)
    page = request.GET.get('page')
    trains = paginator.get_page(page)
    return render(request, 'trains/home.html', {'objects_list': trains})


class TrainDetailView(DetailView):
    queryset = Train.objects.all()    # pylint: disable=maybe-no-member
    context_object_name = 'object'
    template_name = 'trains/detail.html'


class TrainCreateView(SuccessMessageMixin, CreateView):
    model = Train
    form_class = TrainForm
    template_name = 'trains/create.html'
    success_url = reverse_lazy('train:home')
    success_message = 'Поезд успешно добавлен!'


class TrainUpdateView(SuccessMessageMixin, UpdateView):
    model = Train
    form_class = TrainForm
    template_name = 'trains/update.html'
    success_url = reverse_lazy('train:home')
    success_message = 'Данные о поезде успешно отредактированы!'


class TrainDeleteView(DeleteView):
    model = Train
    success_url = reverse_lazy('train:home')

    def get(self, request, *args, **kwargs):
        messages.success(request, 'Поезд успешно удалён')
        return self.post(request, *args, **kwargs)
