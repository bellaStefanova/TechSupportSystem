from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class StatusOptions(models.TextChoices):
    WAITING = 'WAITING', 'Waiting'
    ASSIGNED = 'ASSIGNED', 'Assigned'
    RESOLVED = 'RESOLVED', 'Resolved'

class Request(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=StatusOptions.choices, default=StatusOptions.WAITING)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super(Request, self).save(*args, **kwargs)
        superusers = UserModel.objects.filter(is_superuser=True)
        notification = RequestNotification(
            request=self,
            message=f'New request created. You can see it here.',
        )
        
        notification.save()
        notification.users_to_notify.set(superusers)
        notification.save()
        for user in superusers:
            user_notification = UserNotification(
                user=user,
                notification=notification,
            )
            user_notification.save()


class RequestNotification(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    users_to_notify = models.ManyToManyField(UserModel)

    def __str__(self):
        return self.message
    
class UserNotification(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    notification = models.ForeignKey(RequestNotification, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)