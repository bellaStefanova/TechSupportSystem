from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from .models import Profile
from TechSupportSystem.notifications.models import RequestNotification

UserModel = get_user_model()

'''these signals are not used, just left here, just in case they are needed in the future'''
# @receiver(post_save, sender=UserModel)
# def user_created(sender, instance, created, *args, **kwargs):
# 	if created:
# 		instance.profile = Profile.objects.create(user=instance)

		
@receiver(post_save, sender=Profile)
def profile_role_modified(sender, instance, created, *args, **kwargs):
    if instance.role.is_eligible_for_staff and not instance.user.is_staff and not instance.user.is_superuser:
        print('test')
        notification = RequestNotification(
            message=f'{instance.user.username} has requested a staff profile with selection of {instance.role} position.',
            notification_type='USER',
            user_submitted_notification=instance.user
        )
        notification.save()
        notification.users_to_notify.set(UserModel.objects.filter(is_superuser=True))
        # notification.user_submitted_notification = instance.user
        notification.save()

# @receiver(post_save, sender=Profile)
# def control_manager(sender, instance, created, *args, **kwargs):
#     role = instance.role
#     if not instance.role.is_eligible_for_staff and instance.user.is_staff:
#         instance.user.is_staff = False
#         instance.user.save()
        

@receiver(post_save, sender=Profile)
def control_staff_option(sender, instance, created, *args, **kwargs):
    if not instance.role.is_eligible_for_staff and instance.user.is_staff:
        instance.user.is_staff = False
        instance.user.save()
        
        

# @receiver(post_save, sender=Profile)
# def 
        
		
