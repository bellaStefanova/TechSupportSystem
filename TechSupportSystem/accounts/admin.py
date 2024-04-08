from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import Profile

UserModel = get_user_model()

@admin.register(UserModel)
class UserModelAdmin(UserAdmin):

    list_display = ['username', 'department', 'email', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active', 'department']
    def has_change_permission(self, request, obj=None):
        # Deny change permission for staff users
        if request.user.is_staff:
            return False
        return True

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'role', 'last_updated_by']
    list_filter = ['role']
    
    def has_change_permission(self, request, obj=None):
        # Deny change permission for staff users
        if request.user.is_staff:
            return False
        return True

