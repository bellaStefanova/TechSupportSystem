from django.db import models
from django.contrib.auth import get_user_model

from TechSupportSystem.notifications.models import RequestNotification

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
    worked_on_by = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='worked_on_by', null=True, blank=True)

    def __str__(self):
        return self.title
    
    # def save(self, take_request=False, request_id=None, taker=None, *args, **kwargs):
    #     '''saving the request if it does not exist'''
        # request = Request.objects.filter(id=request_id)
        # if not request:
        #     request = super(Request, self).save(*args, **kwargs)
        #     notification = RequestNotification(
        #         request=self,
        #         message=f'New request created.',
        #     )
        #     notification.save()

        #     superusers = UserModel.objects.filter(is_superuser=True)
        #     notification.users_to_notify.set(superusers)
        #     notification.save()

        # else:
        #     if take_request:
        #         request = self
        #         request.worked_on_by = taker
        #         request.status = StatusOptions.ASSIGNED[1]
                
        # request_obj, created = Request.objects.update_or_create(
        #     id=request_id,
        # )


            # print(request)



        # super(Request, self).save(*args, **kwargs)
        # superusers = UserModel.objects.filter(is_superuser=True)
        # if create_notification:
        #     request = super(Request, self).save(*args, **kwargs)
        #     notification = RequestNotification(
        #         request=self,
        #         message=f'New request created.',
        #     )
            
        #     notification.save()
        #     notification.users_to_notify.set(superusers)
        #     notification.save()
        #     for user in superusers:
        #         user_notification = UserNotification(
        #             user=user,
        #             notification=notification,
        #         )
        #         user_notification.save()
        # else:
        #     # print(request_id)
        #     support_request = self
        #     print(support_request)
        #     support_request.worked_on_by = UserModel.objects.get(id=user_id)
        #     support_request.status = StatusOptions.ASSIGNED[1]
        #     support_request.save()
        #     notification = RequestNotification(
        #         request=request,
        #         message=f'New request assigned to you.',
        #     )
        #     users_to_notify = UserModel.objects.filter(request=support_request)
        #     notification.save(commit=False)
        #     notification.users_to_notify.add(users_to_notify)
        #     notification.save()
        # return super(Request, self).save(*args, **kwargs)


