
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('TechSupportSystem.web.urls')),
    path('', include('TechSupportSystem.admin.urls')),
    path('', include('TechSupportSystem.accounts.urls')),
    path('', include('TechSupportSystem.requests.urls')),
    path('', include('TechSupportSystem.notifications.urls')),
    path('', include('TechSupportSystem.departments.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
