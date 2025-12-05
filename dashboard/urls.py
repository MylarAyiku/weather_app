from django.urls import path
from .views  import WeatherView, NewsView


urlpatterns=[
    path('weather/', WeatherView.as_view(), name='weather'),
    path('news/', NewsView.as_view(), name='news'),
]