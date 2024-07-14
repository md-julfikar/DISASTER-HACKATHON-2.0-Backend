from django.core.management.base import BaseCommand
from app.task import fetch_data_from_api

class Command(BaseCommand):
    help = 'Manually run fetch_data_from_api to test job scheduling'

    def handle(self, *args, **options):
        fetch_data_from_api()
        self.stdout.write(self.style.SUCCESS('Successfully ran fetch_data_from_api'))