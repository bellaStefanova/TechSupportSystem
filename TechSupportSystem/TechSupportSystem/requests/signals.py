from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
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
        )
        notification.save()

        superusers = UserModel.objects.filter(is_superuser=True)
        notification.users_to_notify.set(superusers)
        notification.save()


@receiver(post_save, sender=Request)
def take_request_handler(sender, instance, **kwargs):

    notification = RequestNotification.objects.filter(
        request=instance,
        message='Request has been taken by {}'.format(instance.worked_on_by),
    )
    if not notification:
        notification = RequestNotification(
            request=instance,
            message='Request has been taken by {}'.format(instance.worked_on_by),
        )
        notification.save()
        notification.users_to_notify.add(instance.user)
        notification.save()
        