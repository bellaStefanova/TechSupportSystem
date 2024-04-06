from django.apps import AppConfig


class DepartmentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'TechSupportSystem.departments'

    def ready(self):
        import TechSupportSystem.departments.management.commands.custom_commands

