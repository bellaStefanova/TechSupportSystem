# Generated by Django 4.2.4 on 2024-03-21 21:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('departments', '0003_role'),
        ('accounts', '0003_userprofile_skip_initial_profile_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='profiles', to='departments.role'),
        ),
        migrations.DeleteModel(
            name='Role',
        ),
    ]
