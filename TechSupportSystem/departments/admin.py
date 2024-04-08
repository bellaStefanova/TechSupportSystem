from django.contrib import admin
from .models import Department, Role


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    
    list_display = ['name', 'location', 'manager']
    list_filter = ['location', ]
    
    
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    
    list_display = ['title', 'department']
    list_filter = ['department']
