from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError
from django.utils.translation import gettext as _
from TechSupportSystem.departments.models import Department

class Command(createsuperuser.Command):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            '--department',
            dest='department',
            type=str,
            help=_('Specifies the department for the superuser.'),
        )

    def handle(self, *args, **options):
        department_name = options.get('department')
        if department_name:
            department, created = Department.objects.get_or_create(name=department_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created department: {department.name}'))
            options['department'] = department

        return super().handle(*args, **options)