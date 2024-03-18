from django.apps import AppConfig


class RequestsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'TechSupportSystem.requests'
    
    def ready(self):
        import TechSupportSystem.requests.signals
