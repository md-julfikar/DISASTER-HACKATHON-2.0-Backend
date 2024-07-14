import logging
import requests
from app.models import WeatherData
logger = logging.getLogger(__name__)

def fetch_data_from_api():
    APIKey = '599d55b51f11471c93963600241205'
    CITY_MAPPING = {
    "Bagerhat": "Bagerhat",
    "Bandarban": "Bandarban",
    "Barguna": "Barguna",
    "Barisal": "Barisal",
    "Bhola": "Bhola",
    "Bogra": "Bogra",
    "Brahmanbaria": "Brahmanbaria",
    "Chandpur": "Chandpur",
    "Chapai Nawabganj": "Nawabganj",
    "Chattogram": "Chittagong",  # Correct API name
    "Chuadanga": "Chuadanga",
    "Cox's Bazar": "Cox's Bazar",
    "Cumilla": "Comilla",  # Correct API name
    "Dhaka": "Dhaka",
    "Dinajpur": "Dinajpur",
    "Faridpur": "Faridpur",
    "Feni": "Feni",
    "Gaibandha": "Gaibandha",
    "Gazipur": "Gazipur",
    "Gopalganj": "Gopalganj",
    "Habiganj": "Habiganj",
    "Jamalpur": "Jamalpur",
    "Jashore": "Jessore",  # Correct API name
    "Jhalokathi": "Jhalokathi",
    "Jhenaidah": "Jhenaidah",
    "Joypurhat": "Joypurhat",
    "Khagrachari": "Khagrachari",
    "Khulna": "Khulna",
    "Kishoreganj": "Kishoreganj",
    "Kurigram": "Kurigram",
    "Kushtia": "Kushtia",
    "Lakshmipur": "Lakshmipur",
    "Lalmonirhat": "Lalmonirhat",
    "Madaripur": "Madaripur",
    "Magura": "Magura",
    "Manikganj": "Manikganj",
    "Meherpur": "Meherpur",
    "Moulvibazar": "Moulvibazar",
    "Munshiganj": "Munshiganj",
    "Mymensingh": "Mymensingh",
    "Naogaon": "Naogaon",
    "Narail": "Narail",
    "Narayanganj": "Narayanganj",
    "Narsingdi": "Narsingdi",
    "Natore": "Natore",
    "Netrokona": "Netrokona",
    "Nilphamari": "Nilphamari",
    "Noakhali": "Noakhali",
    "Pabna": "Pabna",
    "Panchagarh": "Panchagarh",
    "Patuakhali": "Patuakhali",
    "Pirojpur": "Pirojpur",
    "Rajbari": "Rajbari",
    "Rajshahi": "Rajshahi",
    "Rangamati": "Rangamati",
    "Rangpur": "Rangpur",
    "Satkhira": "Satkhira",
    "Shariatpur": "Shariatpur",
    "Sherpur": "Sherpur",
    "Sirajganj": "Sirajganj",
    "Sunamganj": "Sunamganj",
    "Sylhet": "Sylhet",
    "Tangail": "Tangail",
    "Thakurgaon": "Thakurgaon"
}


    timeout = 3
    weather_data_list = []
    for city,api_city in CITY_MAPPING.items():
        url = f'http://api.weatherapi.com/v1/current.json?key={APIKey}&q={api_city}'
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status() 
            data = response.json()
            if 'error' not in data:
                weather_data = WeatherData(
                    city_name=str(data['location']['name']).lower(),
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