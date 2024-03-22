from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from .models import Profile

UserModel = get_user_model()

'''these signals are not used, just left here, just in case they are needed in the future'''
@receiver(post_save, sender=UserModel)
def user_created(sender, instance, created, *args, **kwargs):
	if created:
		instance.profile = Profile.objects.create(user=instance)

		
@receiver(post_save, sender=Profile)
def profile_role_modified(sender, instance, created, *args, **kwargs):
    if instance.role == "Team lead":
        instance.user.is_staff = True
        instance.user.save()
        
		
