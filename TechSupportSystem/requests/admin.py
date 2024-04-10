from django.contrib import admin
from .models import Request

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):

    list_display = ['title', 'urgency', 'status', 'user', 'last_updated_by']
    list_filter = ['status', 'urgency', 'user']
