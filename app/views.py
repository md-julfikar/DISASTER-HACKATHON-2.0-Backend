from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import WeatherData
from .serializers import WeatherDataSerializer

@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('city', openapi.IN_QUERY, description="City name", type=openapi.TYPE_STRING, required=True),
        openapi.Parameter('days_ago', openapi.IN_QUERY, description="Days ago", type=openapi.TYPE_INTEGER, required=False)
    ],
    responses={
        200: WeatherDataSerializer(many=True),
        400: 'Bad Request',
        404: 'Not Found'
    }
)
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
def home(request):
    return render(request, 'index.html')
