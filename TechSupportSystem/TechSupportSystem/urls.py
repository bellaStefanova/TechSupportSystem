
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('TechSupportSystem.accounts.urls')),
    path('', include('TechSupportSystem.requests.urls')),
    path('', include('TechSupportSystem.notifications.urls')),
]
