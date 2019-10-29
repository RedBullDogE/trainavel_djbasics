from django.urls import path
from . import views

urlpatterns = [
    path('detail/<int:pk>/', views.CityDetailView.as_view(), name='detail'),
    path('add/', views.CityCreateView.as_view(), name='add'),
    path('', views.home, name='home')
]