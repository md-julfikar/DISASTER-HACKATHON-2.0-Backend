from django.db import models
from django.utils import timezone

class WeatherData(models.Model):
    city_name = models.CharField(max_length=50)
    date = models.DateField()
    time = models.TimeField()
    temp = models.FloatField()
    humidity = models.CharField(max_length=10)
    heatindex = models.CharField(max_length=15)
    condition = models.CharField(max_length=20)
    wind_speed = models.CharField(max_length=15)
    gust_speed = models.CharField(max_length=10)
    pressure = models.CharField(max_length=15)
    cloud = models.CharField(max_length=10)
    precip = models.CharField(max_length=15)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.city_name}-{self.condition}-{self.date}"
