
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('TechSupportSystem.web.urls')),
    path('', include('TechSupportSystem.admin.urls')),
    path('', include('TechSupportSystem.accounts.urls')),
    path('', include('TechSupportSystem.requests.urls')),
    path('', include('TechSupportSystem.notifications.urls')),
    path('', include('TechSupportSystem.departments.urls')),
    
]
