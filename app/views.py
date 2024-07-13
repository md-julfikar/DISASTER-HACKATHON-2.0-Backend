from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import WeatherData
from django.utils import timezone
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import WeatherDataSerializer
from datetime import timedelta

@api_view(['GET'])
def WeatherView(request):
    city = str(request.GET.get('city')).lower()
    days_ago = request.GET.get('days_ago', 0) 

    if not city:
        return Response(status=400, data={"message": "City parameter is required"})

    try:
        days_ago = int(days_ago)
    except ValueError:
        return Response(status=400, data={"message": "days_ago must be an integer"})

    now = timezone.localtime(timezone.now())
    target_date = now.date() - timedelta(days=days_ago)
    print(f"Current date: {now.date()}, Target date: {target_date}")

    weather_data = WeatherData.objects.filter(city_name=city, date=target_date)
    if not weather_data.exists():
        return Response(status=404, data={"message": "No data found for the given city and date"})

    serializer = WeatherDataSerializer(weather_data, many=True)
    return Response(serializer.data)
