from django.shortcuts import render
from weather_app.services import WeatherService
from django.http import JsonResponse


def coolest_places(request):
    res = WeatherService().get_coolest_districts()
    return JsonResponse(res, safe=False)

def temperature_info(request):
    pass