from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.contrib.auth import get_user_model
from .models import Profile
from TechSupportSystem.notifications.models import RequestNotification

UserModel = get_user_model()

@receiver(pre_save, sender=Profile)
def track_changes(sender, instance, **kwargs):
    changed_fields = []
    try:
        old_instance = Profile.objects.get(pk=instance.pk)
    except Profile.DoesNotExist:
        return

    for field in instance._meta.fields:
        if getattr(instance, field.attname) != getattr(old_instance, field.attname):
            changed_fields.append(field.attname)

    if changed_fields:
        if 'role_id' in changed_fields and not instance.last_updated_by.is_superuser:
            department = instance.user.department
            if instance.role == department.management_role and instance.last_updated_by == instance.user:
                notification = RequestNotification(
                    message=f'{instance.user.username} has registered as {instance.role} of {department} department.\nClick here to edit their profile',
                    notification_type='USER',
                    user_submitted_notification=instance.last_updated_by
                )
                notification.save()
                notification.users_to_notify.set(UserModel.objects.filter(is_superuser=True))
                notification.save()
        elif 'first_name' in changed_fields or 'last_name' in changed_fields or 'role_id' in changed_fields and instance.last_updated_by.is_superuser:
            if instance.last_updated_by.is_superuser:
                notification = RequestNotification(
                    message=f'Your profile has been updated by {instance.last_updated_by}.\n Go to profile details to see the changes.',
                    notification_type='USER',
                    user_submitted_notification=instance.last_updated_by #this is not correct but won't be used so it's fine for now
                )
                notification.save()
                notification.users_to_notify.add(instance.user)
                notification.save()
                
            
@receiver(pre_save, sender=UserModel)
def track_changes(sender, instance, **kwargs):
    changed_fields = []
    try:
        old_instance = UserModel.objects.get(pk=instance.pk)
    except UserModel.DoesNotExist:
        return

    for field in instance._meta.fields:
        if getattr(instance, field.attname) != getattr(old_instance, field.attname):
            changed_fields.append(field.attname)
    
    if 'is_staff' in changed_fields:
        if instance.is_staff:
            notification = RequestNotification(
                message=f'Your level has been updated to manager.\n You can now see your team members and their requests.',
                notification_type='USER',
                user_submitted_notification=instance.profile.last_updated_by #this is not correct but won't be used so it's fine for now
            )
            notification.save()
            notification.users_to_notify.add(instance)
            notification.save()
        elif not instance.is_staff:
            notification = RequestNotification(
                message=f'Your manager level has been deleted.\n You can see the change in your profile details.',
                notification_type='USER',
                user_submitted_notification=instance.profile.last_updated_by #this is not correct but won't be used so it's fine for now
            )
            notification.save()
            notification.users_to_notify.add(instance)
            notification.save()
    elif 'email' in changed_fields or 'department_id' in changed_fields:
            if instance.profile.last_updated_by.is_superuser:
                notification = RequestNotification(
                    message=f'Your profile has been updated by {instance.profile.last_updated_by}.\n Go to profile details to see the changes.',
                    notification_type='USER',
                    user_submitted_notification=instance.profile.last_updated_by #this is not correct but won't be used so it's fine for now
                )
                notification.save()
                notification.users_to_notify.add(instance)
                notification.save()

		
