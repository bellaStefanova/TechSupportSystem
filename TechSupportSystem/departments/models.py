from django.db import models
# from django.contrib.auth import get_user_model
# from TechSupportSystem.accounts.models import UserProfile

# UserModel = UserProfile

class Department(models.Model):
    DEPARTMENT_MAX_LENGTH = 50
    LOCATION_MAX_LENGTH = 50

    name = models.CharField(
        max_length=DEPARTMENT_MAX_LENGTH,
        unique=True,
    )

    description = models.TextField(
    )
    
    management_role = models.ForeignKey(
        'departments.Role',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_departments',
    )

    manager = models.ForeignKey(
        'accounts.UserProfile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_departments',
    )

    location = models.CharField(
        max_length=LOCATION_MAX_LENGTH,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.name


'''Role Model for employees positions'''

class Role(models.Model):
        
    TITLE_MAX_LENGTH = 50
    DESCRIPTION_MAX_LENGTH = 150
    
    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
    )

    description = models.TextField(
        max_length=DESCRIPTION_MAX_LENGTH,
    )

    # is_eligible_for_staff = models.BooleanField(
    #     default=False,
    # )
    
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        related_name='roles',
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title