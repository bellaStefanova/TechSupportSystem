from django.apps import AppConfig


class AccountsConfig(AppConfig):
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'TechSupportSystem.accounts'
    
    def ready(self):
        import TechSupportSystem.accounts.signals