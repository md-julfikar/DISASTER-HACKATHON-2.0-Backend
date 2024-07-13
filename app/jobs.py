from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
import requests
from .models import WeatherData

def fetch_data_from_api():
    APIKey = '599d55b51f11471c93963600241205'
    districts = [
        "Bagerhat", "Bandarban", "Barguna", "Barisal", "Bhola", "Bogra", "Brahmanbaria", 
        "Chandpur", "Chapai Nawabganj", "Chattogram", "Chuadanga", "Cox's Bazar", "Cumilla",
        "Dhaka", "Dinajpur", "Faridpur", "Feni", "Gaibandha", "Gazipur", "Gopalganj", 
        "Habiganj", "Jamalpur", "Jashore", "Jhalokathi", "Jhenaidah", "Joypurhat", 
        "Khagrachari", "Khulna", "Kishoreganj", "Kurigram", "Kushtia", "Lakshmipur", 
        "Lalmonirhat", "Madaripur", "Magura", "Manikganj", "Meherpur", "Moulvibazar", 
        "Munshiganj", "Mymensingh", "Naogaon", "Narail", "Narayanganj", "Narsingdi", 
        "Natore", "Netrokona", "Nilphamari", "Noakhali", "Pabna", "Panchagarh", 
        "Patuakhali", "Pirojpur", "Rajbari", "Rajshahi", "Rangamati", "Rangpur", 
        "Satkhira", "Shariatpur", "Sherpur", "Sirajganj", "Sunamganj", "Sylhet", 
        "Tangail", "Thakurgaon"
    ]

    for city in districts:
        url = f'http://api.weatherapi.com/v1/current.json?key={APIKey}&q={city}'
        response = requests.get(url)
        data = response.json()
        if 'error' not in data:
            WeatherData.objects.create(
                city_name=data['location']['name'],
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

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(fetch_data_from_api, 'interval', hours=1, name='fetch_data_from_api', jobstore='default')

    register_events(scheduler)

    scheduler.start()
