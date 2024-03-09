from django.db import models
from django.contrib.auth import models as auth_models, get_user_model

from TechSupportSystem.departments.models import Department


'''Custom User Model'''
class UserProfile(auth_models.AbstractUser):
    department = models.ForeignKey(
        Department,
        on_delete=models.DO_NOTHING,
        related_name='employees',
        null=True,
        blank=True,
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
        'Role',
        on_delete=models.DO_NOTHING,
        related_name='profiles',
        null=True,
        blank=True,
    )


'''Role Model for employees positions'''

class Role(models.Model):
        
        TITLE_MAX_LENGTH = 50
        DESCRIPTION_MAX_LENGTH = 1000
    
        title = models.CharField(
            max_length=TITLE_MAX_LENGTH,
        )

        description = models.TextField(
            max_length=DESCRIPTION_MAX_LENGTH,
        )

        is_eligible_for_staff = models.BooleanField(
            default=False,
        )
    
