from django.core.management.base import BaseCommand
from jobs.jobs import get_data

class Command(BaseCommand):
    help = 'Collect weather data'

    def handle(self, *args, **options):
        get_data()
        self.stdout.write(self.style.SUCCESS('Successfully collected data'))