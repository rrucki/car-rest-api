from django.urls import path
from .views import car_list, car_detail, rating, popularity

urlpatterns = [
    path('cars/', car_list, name='cars'),
    path('cars/<int:pk>/', car_detail, name='delete'),
    path('rate/', rating, name='rate'),
    path('popular/', popularity, name='popular')
]
