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
    city = request.GET.get('city')
    days_ago = request.GET.get('days_ago')

    if not city or not days_ago:
        return Response(status=400, data={"message": "City and days_ago parameters are required"})

    try:
        days_ago = int(days_ago)
    except ValueError:
        return Response(status=400, data={"message": "days_ago must be an integer"})

    target_date = timezone.now().date() - timedelta(days=days_ago)

    try:
        weather_data = WeatherData.objects.filter(city_name=city, date=target_date)
        if not weather_data.exists():
            return Response(status=404, data={"message": "No data found for the given city and date"})

        serializer = WeatherDataSerializer(weather_data, many=True)
        return Response(serializer.data)
    except WeatherData.DoesNotExist:
        return Response(status=404, data={"message": "City not found"})
