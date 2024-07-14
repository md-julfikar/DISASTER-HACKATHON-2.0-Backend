from django.apps import AppConfig
from django.db.models.signals import post_migrate

class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        from .jobs import start_scheduler
        post_migrate.connect(start_scheduler, sender=self)
