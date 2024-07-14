from django.conf import settings
import logging
import requests
from app.models import WeatherData
logger = logging.getLogger(__name__)


def get_data():
    APIKey = '599d55b51f11471c93963600241205'
    CITY_MAPPING = {
        "Chittagong": "Chattogram", "Comilla":"Cumilla","Jessore":"Jashore"
    }

    citys=['Bagerhat', 'Bandarban', 'Barisal', 'Bhola', 'Bogra', 'Brahmanbaria', 'Chandpur', 'Nawabganj', 'Chittagong', "Cox's Bazar", 'Comilla', 'Dhaka', 'Dinajpur', 'Faridpur', 'Feni', 'Gazipur', 'Gopalganj', 'Habiganj', 'Jamalpur', 'Jessore', 'Khagrachari', 'Khulna', 'Kishoreganj', 'Kushtia', 'Lakshmipur', 'Lalmonirhat', 'Madaripur', 'Magura', 'Manikganj', 'Munshiganj', 'Mymensingh', 'Naogaon', 'Narail', 'Narayanganj', 'Narsingdi', 'Noakhali', 'Pabna', 'Panchagarh', 'Patuakhali', 'Pirojpur', 'Rajbari', 'Rajshahi', 'Rangamati', 'Rangpur', 'Satkhira', 'Sherpur', 'Sirajganj', 'Sunamganj', 'Sylhet', 'Tangail', 'Thakurgaon']
    timeout = 3
    weather_data_list = []
    for city in citys:
        if city in CITY_MAPPING:
            url = f'http://api.weatherapi.com/v1/current.json?key={APIKey}&q={CITY_MAPPING[city]}'
        else:
            url = f'http://api.weatherapi.com/v1/current.json?key={APIKey}&q={city}'
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status() 
            data = response.json()
            if 'error' not in data:
                weather_data = WeatherData(
                    city_name=CITY_MAPPING[city].lower() if city in CITY_MAPPING else city.lower(),
                    date=data['location']['localtime'].split(' ')[0],
                    time=data['location']['localtime'].split(' ')[1],
                    temp=data['current']['temp_c'],
                    humidity=data['current']['humidity'],
                    heatindex=data['current']['feelslike_c'],
                    condition=data['current']['condition']['text'],
                    wind_speed=data['current']['wind_kph'],
                    gust_speed=data['current']['gust_kph'],
                    pressure=data['current']['pressure_mb'],
                    cloud=data['current']['cloud'],
                    precip=data['current']['precip_mm'],
                )
                weather_data_list.append(weather_data)
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data for {city}: {e}")

    if weather_data_list:
        WeatherData.objects.bulk_create(weather_data_list)