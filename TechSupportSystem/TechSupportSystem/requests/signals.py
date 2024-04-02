from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from .models import Request
from TechSupportSystem.notifications.models import RequestNotification

UserModel = get_user_model()


@receiver(post_save, sender=Request)
def request_created(sender, instance, created, *args, **kwargs):
    if created:
        notification = RequestNotification(
        request=instance,
            message=f'New request created.',
            notification_type='REQUEST',
            user_submitted_notification = instance.user
        )
        notification.save()

        superusers = UserModel.objects.filter(is_superuser=True)
        notification.users_to_notify.set(superusers)
        notification.save()


@receiver(post_save, sender=Request)
def take_request_handler(sender, instance, created, **kwargs):

    if not created:
        if instance.worked_on_by:
            notification = RequestNotification.objects.filter(
                request=instance,
                message=f'Request has been taken by {instance.worked_on_by}',
                notification_type='REQUEST',
            )
            if not notification:
                notification = RequestNotification(
                    request=instance,
                    message=f'Request has been taken by {instance.worked_on_by}',
                    notification_type='REQUEST',
                    user_submitted_notification = instance.worked_on_by
                )
                notification.save()
                notification.users_to_notify.add(instance.user)
                notification.save()

 
@receiver(post_save, sender=Request)
def edit_request_handler(sender, instance, created, **kwargs):

    if not created:
        notification = RequestNotification(
            request=instance,
                    notification_type='REQUEST',
                    user_submitted_notification = instance.last_updated_by
        )
        notification.save()
                    
        ''' Marking with Resolved should send a notification to the user who submitted the request
        saying that the request has been resolved by the superuser who resolved it. '''
        if instance.status == 'Resolved':
            notification.message = f'Request has been marked as resolved by {instance.last_updated_by}'
            notification.users_to_notify.add(instance.user)
            notification.save()
        
        ### if the request is cancelled by superuser, a notification is sent to the user who submitted 
        # the request
        elif instance.status == 'Cancelled':
            notification.message = f'Request has been cancelled by {instance.last_updated_by}'
            
            if instance.last_updated_by.is_superuser:
                notification.users_to_notify.add(instance.user)
            else:
                notification.users_to_notify.set(UserModel.objects.filter(is_superuser=True))
                
            notification.save()
        
        else:
            notification.message = f'Request has been updated by {instance.last_updated_by}'
            if instance.last_updated_by.is_superuser:
                notification.users_to_notify.add(instance.user)
            else:
                notification.users_to_notify.set(UserModel.objects.filter(is_superuser=True))
            notification.save()
                
