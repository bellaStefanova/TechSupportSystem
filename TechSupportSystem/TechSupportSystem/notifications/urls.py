from django.urls import path
from .views import ListNotificationView, MarkNotificationAsReadView

urlpatterns = (
    (path('view-notifications/', ListNotificationView.as_view(), name='view-notifications')),
    (path('mark-notification-as-read/<int:notification_id>/', MarkNotificationAsReadView.as_view(), name='mark_notification_as_read')),

)