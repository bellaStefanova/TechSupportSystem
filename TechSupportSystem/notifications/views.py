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
        max_notifications = 20
        
        read_notifications = UserNotification.objects.filter(
            user=self.request.user, 
            is_read=True, 
            notification__notification_type='REQUEST'
        ).order_by('-notification__created_at')
        
        user_notifications = UserNotification.objects.filter(
            user=self.request.user, 
            is_read=False, 
            notification__notification_type='USER'
        ).order_by('-notification__created_at')
        
        context['read_notifications'] = read_notifications
        context['user_notifications'] = user_notifications
        
        if context['unread_notifications'].count() >= max_notifications:
            context['unread_notifications'] = context['unread_notifications'][:max_notifications]
        else:
            context['read_notifications'] = context['read_notifications'][:(max_notifications - context['unread_notifications'].count())]

        return context
    

class MarkNotificationAsReadView(GetNotificationsMixin, View):
    
    def post(self, request, notification_id):

        user_notification = UserNotification.objects.get(id=notification_id)
        user_notification.is_read = True
        user_notification.save()
        
        return JsonResponse({'message': 'Notification marked as read'}, status=200)


    def get(self, request, *args, **kwargs):

        return JsonResponse({'error': 'Invalid request method'}, status=400)



class ReadAllNotificationsView(GetNotificationsMixin, View):
    
    def post(self, request):
        
        user_notifications = UserNotification.objects.filter(user=request.user, is_read=False, notification__notification_type='REQUEST')
        for notification in user_notifications:
            notification.is_read = True
            notification.save()
            
        return JsonResponse({'message': 'All notifications marked as read'}, status=200)
    
    
    def get(self, request, *args, **kwargs):

        return JsonResponse({'error': 'Invalid request method'}, status=400)
    