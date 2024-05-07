from django.shortcuts import render
import requests
from .utils import get_weather, get_city_from_user
from django.views.generic import TemplateView


def weather(request):
    city = request.GET.get('city', 'Kyiv')
    weather_data = get_weather(city)
    context = {'weather': weather_data}
    return render(request, 'weather.html', context)


def weather_view(request):
    return render(request, 'weather.html')


class WeatherView(TemplateView):
    template_name = 'weather.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        city = self.request.GET.get('city', 'Kyiv')  # We get the name of the city from the GET parameter 'city', if not specified, we use 'Kyiv' by default
        weather_data = get_weather(city)  # We receive weather data for the specified city
        context['weather'] = weather_data  # Adding weather data to context
        context['city'] = city
        return context