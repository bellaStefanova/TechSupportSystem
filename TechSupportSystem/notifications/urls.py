from django.urls import path
from .views import ListNotificationView, MarkNotificationAsReadView, ReadAllNotificationsView, fetch_notifications

urlpatterns = (
    (path('view-notifications/', ListNotificationView.as_view(), name='view-notifications')),
    (path('mark-notification-as-read/<int:notification_id>/', MarkNotificationAsReadView.as_view(), name='mark_notification_as_read')),
    (path('mark-all-notifications-as-read/', ReadAllNotificationsView.as_view(), name='mark_all_notifications_as_read')),
    (path('fetch-notifications/', fetch_notifications, name='fetch_notifications')),
)