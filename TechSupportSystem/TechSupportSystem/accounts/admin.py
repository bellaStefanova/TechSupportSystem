from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from .models import Profile, Role

UserModel = get_user_model()

@admin.register(UserModel)
class UserModelAdmin(auth_admin.UserAdmin):
    pass
    # list_display = ['__all__',]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    pass