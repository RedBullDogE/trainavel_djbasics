from django.contrib import admin
from .models import Route


class RouteAdmin(admin.ModelAdmin):
    class Meta:
        model = Route
    list_display = ('name', 'from_city', 'to_city',
                    'get_cities', 'travel_time')

    def get_cities(self, obj):
        return "\n".join([c.name for c in obj.across_cities.all()])


admin.site.register(Route, RouteAdmin)
