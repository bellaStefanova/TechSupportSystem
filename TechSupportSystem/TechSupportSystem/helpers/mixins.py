from django.views import generic as views
from django.contrib.auth.mixins import LoginRequiredMixin

from TechSupportSystem.notifications.models import RequestNotification, UserNotification
from TechSupportSystem.departments.models import Department

class GetNotificationsMixin(LoginRequiredMixin,views.base.ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # unread_notifications = RequestNotification.objects.filter(user=self.request.user, is_read=False).order_by('-notification__created_at')
        unread_notifications = UserNotification.objects.filter(
            user=self.request.user,
            is_read=False
        ).order_by('-notification__created_at')
        departments = Department.objects.filter(manager=self.request.user)
        context['notifications'] = len(unread_notifications)
        context['unread_notifications'] = unread_notifications.filter(notification__notification_type='REQUEST')
        context['departments'] = departments
        return context
    
class VisibleToSuperUserMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class VisibleToStaffMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

def get_request_model():
    from TechSupportSystem.requests.models import Request
    return Request