from django.views import generic as views
from django.contrib.auth.mixins import LoginRequiredMixin

from TechSupportSystem.notifications.models import RequestNotification, UserNotification

class GetNotificationsMixin(LoginRequiredMixin,views.base.ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # unread_notifications = RequestNotification.objects.filter(user=self.request.user, is_read=False).order_by('-notification__created_at')
        unread_notifications = UserNotification.objects.filter(
            user=self.request.user,
            is_read=False
        ).order_by('-notification__created_at')
        context['notifications'] = len(unread_notifications)
        context['unread_notifications'] = unread_notifications
        return context

def get_request_model():
    from TechSupportSystem.requests.models import Request
    return Request