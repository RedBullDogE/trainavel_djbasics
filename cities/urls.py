from django.urls import path
from . import views

urlpatterns = [
    path('detail/<int:pk>/', views.CityDetailView.as_view(), name='detail'),
    path('', views.home, name='home')
]