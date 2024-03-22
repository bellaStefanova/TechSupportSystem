from django.db import models
from django.contrib.auth import models as auth_models, get_user_model

from TechSupportSystem.departments.models import Department, Role


'''Custom User Model'''
class UserProfile(auth_models.AbstractUser):
    
    department = models.ForeignKey(
        Department,
        on_delete=models.DO_NOTHING,
        related_name='employees',
        null=True,
        blank=True,
    )
    
    skip_initial_profile_details = models.BooleanField(
        default=False,
    )


'''Profile Model related to UserProfile, extenging its information with non-required one'''
UserModel = get_user_model()


class Profile(models.Model):

    FIRST_NAME_MAX_LENGTH = 50
    LAST_NAME_MAX_LENGTH = 50

    user = models.OneToOneField(
        UserModel, 
        on_delete=models.DO_NOTHING,
        related_name='profile',
    )

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
    )

    role = models.ForeignKey(
        Role,
        on_delete=models.DO_NOTHING,
        related_name='profiles',
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
