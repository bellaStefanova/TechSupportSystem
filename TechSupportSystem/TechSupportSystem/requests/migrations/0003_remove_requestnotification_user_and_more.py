# Generated by Django 4.2.4 on 2024-03-13 16:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('requests', '0002_requestnotification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requestnotification',
            name='user',
        ),
        migrations.AddField(
            model_name='requestnotification',
            name='users_to_notify',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
