from django.shortcuts import render
from django.contrib import messages
from trains.models import Train
from cities.models import City
from .forms import RouteForm


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
            all_ways = list(dfs_paths(graph, from_city.id, to_city.id))
            if not all_ways:
                messages.error(
                    request, 'Маршрута, удовлетворяющего условиям, не существует')
                return render(request, 'routes/home.html', {'form': form})
            if across_cities_form:
                across_cities = [city.id for city in across_cities_form]
                right_ways = []
                for way in all_ways:
                    if all(point in way for point in across_cities):
                        right_ways.append(way)
                if not right_ways:
                    messages.error(
                        request, 'Маршрут через заданные города невозможен')
                    return render(request, 'routes/home.html', {'form': form})
            else:
                right_ways = all_ways

        trains = [
            [Train.objects.filter(
                from_city=way[i],
                to_city=way[i+1]
            ).order_by('travel_time').first() for i in range(len(way) - 1)]
            for way in right_ways]
        travel_time = [sum([train.travel_time for train in way]) for way in trains]
        # --- test ---
        cities = City.objects.all()
        for way in right_ways:
            for i in range(len(way)):
                way[i] = City.objects.get(id=way[i]).name

        context = {'form': RouteForm, 'ways': right_ways}
        return render(request, 'routes/home.html', context)
    else:
        messages.error(request, 'Создайте маршрут')
        form = RouteForm()
        return render(request, 'routes/home.html', {'form': form})
