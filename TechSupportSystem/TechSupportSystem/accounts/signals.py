from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from .models import Profile
from TechSupportSystem.notifications.models import RequestNotification
from TechSupportSystem.departments.models import Department

UserModel = get_user_model()

'''these signals are not used, just left here, just in case they are needed in the future'''
# @receiver(post_save, sender=UserModel)
# def user_created(sender, instance, created, *args, **kwargs):
# 	if created:
# 		instance.profile = Profile.objects.create(user=instance)

		
@receiver(post_save, sender=Profile)
def profile_role_modified(sender, instance, created, *args, **kwargs):
    department = instance.user.department
    # if instance.role.is_eligible_for_staff and not instance.user.is_staff and not instance.user.is_superuser:
    if instance.role == department.management_role and instance.last_updated_by == instance.user and not instance.user.is_superuser:
        notification = RequestNotification(
            message=f'{instance.user.username} has registered as {instance.role} of {department} department.',
            notification_type='USER',
            user_submitted_notification=instance.user
        )
        notification.save()
        notification.users_to_notify.set(UserModel.objects.filter(is_superuser=True))
        # notification.user_submitted_notification = instance.user
        notification.save()
    if instance.last_updated_by.is_superuser and instance.user.is_staff:
        notification = RequestNotification(
            message=f'Your role has been updated to staff.\n You can now see your team members and their requests.',
            notification_type='USER',
            user_submitted_notification=instance.user #this is not correct but won't be used so it's fine for now
        )
        notification.save()
        notification.users_to_notify.add(instance.user)
        notification.save()

# @receiver(post_save, sender=Profile)
# def control_manager(sender, instance, created, *args, **kwargs):
#     role = instance.role
#     if not instance.role.is_eligible_for_staff and instance.user.is_staff:
#         instance.user.is_staff = False
#         instance.user.save()
        

# @receiver(post_save, sender=Profile)
# def control_staff_option(sender, instance, created, *args, **kwargs):
#     if not instance.role.is_eligible_for_staff and instance.user.is_staff:
#         instance.user.is_staff = False
#         instance.user.save()
        
        

# @receiver(post_save, sender=Profile)
# def 
        
		
