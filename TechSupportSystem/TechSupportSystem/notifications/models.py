from django.db import models
from django.contrib.auth import get_user_model

# from TechSupportSystem.helpers.mixins import get_request_model

# from TechSupportSystem.requests.models import Request


UserModel = get_user_model()
# RequestModel = get_request_model()

class RequestNotification(models.Model):
    request = models.ForeignKey('requests.Request', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    users_to_notify = models.ManyToManyField(UserModel, through='UserNotification')
    # is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message
    
    
class UserNotification(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    notification = models.ForeignKey('RequestNotification', on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)