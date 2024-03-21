from django.shortcuts import render
from django.views import generic as views
from django.views import View
from django.http import JsonResponse

from TechSupportSystem.helpers.mixins import GetNotificationsMixin
from .models import RequestNotification, UserNotification


class ListNotificationView(GetNotificationsMixin, views.ListView):
    queryset = RequestNotification.objects.all()
    template_name = 'requests/view-notifications.html'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        read_notifications = UserNotification.objects.filter(user=self.request.user, is_read=True).order_by('-notification__created_at')
        context['read_notifications'] = read_notifications
        return context
    


class MarkNotificationAsReadView(View):
    def post(self, request, notification_id):

        user_notification = UserNotification.objects.get(id=notification_id)
        user_notification.is_read = True
        user_notification.save()
        return JsonResponse({'message': 'Notification marked as read'}, status=200)

    def get(self, request, *args, **kwargs):
        print('GET')
        return JsonResponse({'error': 'Invalid request method'}, status=400)