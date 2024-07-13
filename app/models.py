from django.db import models
from django.utils import timezone

class WeatherData(models.Model):
    city_name = models.CharField(max_length=50)
    date = models.DateField()
    time = models.TimeField()
    temp = models.CharField(max_length=50)
    humidity = models.CharField(max_length=50)
    heatindex = models.CharField(max_length=50)
    condition = models.CharField(max_length=50)
    wind_speed = models.CharField(max_length=50)
    gust_speed = models.CharField(max_length=50)
    pressure = models.CharField(max_length=50)
    cloud = models.CharField(max_length=50)
    precip = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.city_name}-{self.condition}-{self.date}"
