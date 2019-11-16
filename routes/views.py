from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib import messages
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy


from trains.models import Train
from cities.models import City
from .models import Route
from .forms import RouteForm, RouteModelForm


def dfs_paths(graph, start, goal):
    """Функция поиска всех возможных маршрутов
       из одного города в другой. Вариант посещения
       одного и того же города более одного раза,
       не рассматривается. 
    """
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        if vertex in graph.keys():
            for next_ in graph[vertex] - set(path):
                if next_ == goal:
                    yield path + [next_]
                else:
                    stack.append((next_, path + [next_]))


def get_graph():
    qs = Train.objects.values('from_city')
    from_city_set = set(i['from_city'] for i in qs)
    graph = {}
    for city in from_city_set:
        trains = Train.objects.filter(from_city=city).values('to_city')
        tmp = set(i['to_city'] for i in trains)
        graph[city] = tmp

    return graph


def home(request):
    form = RouteForm()
    return render(request, 'routes/home.html', {'form': form})


def find_routes(request):
    if request.method == "POST":
        form = RouteForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            from_city = data['from_city']
            to_city = data['to_city']
            across_cities_form = data['across_cities']
            travel_time = data['travel_time']

            graph = get_graph()
            all_ways_list = list(dfs_paths(graph, from_city.id, to_city.id))

            if not all_ways_list:
                messages.error(
                    request, 'Маршрута, удовлетворяющего условиям, не существует')
                return render(request, 'routes/home.html', {'form': form})

            if across_cities_form:
                across_cities = [city.id for city in across_cities_form]
                ways_with_cities_list = []
                for way in all_ways_list:
                    if all(point in way for point in across_cities):
                        ways_with_cities_list.append(way)
                if not ways_with_cities_list:
                    messages.error(
                        request, 'Маршрут через заданные города невозможен')
                    return render(request, 'routes/home.html', {'form': form})
            else:
                ways_with_cities_list = all_ways_list

            trains_list = [
                [Train.objects.filter(
                    from_city=way[i],
                    to_city=way[i+1]
                ).order_by('travel_time').first() for i in range(len(way) - 1)]
                for way in ways_with_cities_list
            ]

            routes = []
            for trains in trains_list:
                routes.append({
                    'route': trains,
                    'total_time': sum([train.travel_time for train in trains]),
                    'from_city': from_city,
                    'to_city': to_city
                })
            routes_with_suitable_time = list(
                filter(lambda x: x['total_time'] <= int(travel_time), routes))

            if not routes_with_suitable_time:
                messages.error(
                    request, 'Время в пути найденных маршрутов больше заданого.')
                return render(request, 'routes/home.html', {'form': form})

            routes_with_suitable_time.sort(key=lambda x: x['total_time'])
            context = {
                'form': RouteForm,
                'routes': routes_with_suitable_time,
                'from_city': from_city,
                'to_city': to_city}
            return render(request, 'routes/home.html', context)
    else:
        messages.error(request, 'Создайте маршрут')
        form = RouteForm()
        return render(request, 'routes/home.html', {'form': form})


def add_route(request):
    if request.method == 'POST':
        form = RouteModelForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            name = data['name']
            travel_time = data['travel_time']
            from_city = data['from_city']
            to_city = data['to_city']
            across_cities = data['across_cities'].split(' ')
            train_id_list = [int(x) for x in across_cities if x.isalnum()]
            qs = Train.objects.filter(id__in=train_id_list)
            route = Route(name=name,
                          from_city=from_city,
                          to_city=to_city,
                          travel_time=travel_time)
            route.save()
            for tr in qs:
                route.across_cities.add(tr.id)
            messages.success(request, 'Маршрут был успешно сохранён')

            return redirect('/')
    else:
        data = request.GET
        if data:
            travel_time = data['travel_time']
            from_city = data['from_city']
            to_city = data['to_city']
            across_cities = data['across_cities'].split(' ')
            train_id_list = [int(x) for x in across_cities if x.isalnum()]
            qs = Train.objects.filter(id__in=train_id_list)
            form = RouteModelForm(initial={
                'from_city': from_city,
                'to_city': to_city,
                'across_cities': data['across_cities'].strip(),
                'travel_time': travel_time})
            route_descriptions = [
                f"Поезд №{train.name} следующий из {train.from_city} в {train.to_city}. Время в пути: {train.travel_time}ч."
                for train in qs
            ]
            context = {
                'form': form,
                'descriptions': route_descriptions,
                'from_city': from_city,
                'to_city': to_city,
                'travel_time': travel_time
            }

            return render(request, 'routes/create.html', context)
        else:
            messages.error(
                request, 'Невозможно сохранить несуществующий маршрут')
            return redirect('/')


class RouteDetailView(DetailView):
    queryset = Route.objects.all()
    context_object_name = 'object'
    template_name = 'routes/detail.html'


class RouteListView(ListView):
    queryset = Route.objects.all()
    # context_object_name = 'object'
    template_name = 'routes/list.html'


class RouteDeleteView(DeleteView):
    model = Route
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        messages.success(request, 'Маршрут успешно удалён')
        return self.post(request, *args, **kwargs)
