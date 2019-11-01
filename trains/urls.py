from django.urls import path
from . import views

urlpatterns = [
    # path('detail/<int:pk>/', views.CityDetailView.as_view(), name='detail'),
    # path('update/<int:pk>/', views.CityUpdateView.as_view(), name='update'),
    # path('delete/<int:pk>/', views.CityDeleteView.as_view(), name='delete'),
    path('add/', views.TrainCreateView.as_view(), name='add'),
    path('', views.home, name='home')
]
