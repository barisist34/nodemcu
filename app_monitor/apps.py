from django.apps import AppConfig


class AppMonitorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_monitor'
    # def ready(self): #241224
    #         from .scheduler import scheduler
    #         scheduler.start()
