from django.db import models
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class StatusOptions(models.TextChoices):
    
    WAITING = 'Waiting', 'Waiting'
    ASSIGNED = 'Assigned', 'Assigned'
    RESOLVED = 'Resolved', 'Resolved'
    CANCELLED = 'Cancelled', 'Cancelled'


class UrgencyOptions(models.TextChoices):
    
    LOW = 'Low', 'Low'
    MEDIUM = 'Medium', 'Medium'
    HIGH = 'High', 'High'
    CRITICAL = 'Critical', 'Critical'


class Request(models.Model):
    
    TITLE_MAX_LENGTH = 100
    URGENCY_MAX_LENGTH = 10
    STATUS_MAX_LENGTH = 10
    
    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
    )
    
    description = models.TextField(
    )
    
    urgency = models.CharField(
        max_length=URGENCY_MAX_LENGTH, 
        choices=UrgencyOptions.choices, 
        default=UrgencyOptions.LOW, 
        null=True, 
        blank=True
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    
    updated_at = models.DateTimeField(
        auto_now=True
    )
    
    status = models.CharField(
        max_length=STATUS_MAX_LENGTH, 
        choices=StatusOptions.choices, 
        default=StatusOptions.WAITING
    )
    
    user = models.ForeignKey(
        UserModel, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
    worked_on_by = models.ForeignKey(
        UserModel, 
        on_delete=models.SET_NULL, 
        related_name='worked_on_by', 
        null=True, 
        blank=True
    )
    
    last_updated_by = models.ForeignKey(
        UserModel, 
        on_delete=models.SET_NULL, 
        related_name='last_updated_by', 
        null=True, 
        blank=True
    )


    def __str__(self):
        
        return self.title
    
