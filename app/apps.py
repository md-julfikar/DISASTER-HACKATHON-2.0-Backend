from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver
class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    def ready(self):
        post_migrate.connect(start_scheduler, sender=self)
    
def start_scheduler(sender, **kwargs):
    from .jobs import start
    start()
