from django.db import models
from django.contrib.auth import get_user_model


UserModel = get_user_model()

class NotificationTypeChoices(models.TextChoices):
    REQUEST = 'Request'
    USER = 'User'

class RequestNotification(models.Model):
    request = models.ForeignKey('requests.Request', on_delete=models.CASCADE, null=True, blank=True)
    user_submitted_notification = models.ForeignKey(UserModel, on_delete=models.SET_NULL, related_name='user_submitted_notification', null=True, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    users_to_notify = models.ManyToManyField(UserModel, through='UserNotification')
    notification_type = models.CharField(max_length=10, choices=NotificationTypeChoices.choices)
    
    def delete(self, *args, **kwargs):
        for user in self.user_submitted_notification.all():
            user.user_submitted_notification = None
            user.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.message
    
    
class UserNotification(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True, blank=True)
    notification = models.ForeignKey('RequestNotification', on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)