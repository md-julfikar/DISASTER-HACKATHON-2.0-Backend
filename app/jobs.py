from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
import requests
from .models import WeatherData
from django.conf import settings

def fetch_data_from_api(start_index=0, end_index=64):
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

    timeout = 3  # Set your desired timeout for the HTTP request in seconds
    for city in districts[start_index:end_index]:
        url = f'http://api.weatherapi.com/v1/current.json?key={APIKey}&q={city}'
        try:
            response = requests.get(url, timeout=timeout)
            data = response.json()
            if 'error' not in data:
                WeatherData.objects.create(
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
        except requests.exceptions.Timeout:
            print(f"Request for {city} timed out after {timeout} seconds.")
def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    job_defaults = settings.APSCHEDULER_JOB_DEFAULTS
    scheduler.configure(job_defaults=job_defaults)

    num_districts = 64
    batch_size = 16 
    for i in range(0, num_districts, batch_size):
        start_index = i
        end_index = min(i + batch_size, num_districts)
        scheduler.add_job(fetch_data_from_api, 'interval', hours=1, args=[start_index, end_index], name=f'fetch_data_from_api_{i}_{end_index}', jobstore='default')

    register_events(scheduler)
    scheduler.start()
