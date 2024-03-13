from django.shortcuts import render
from django.views import generic as views
from .models import Request, RequestNotification, UserNotification
from django.forms import modelform_factory
from django.urls import reverse_lazy

class CreateRequestView(views.CreateView):
    queryset = Request.objects.all()
    form_class = modelform_factory(Request, exclude=('status', 'user'))
    template_name = 'requests/create-request.html'

    def get_success_url(self) -> str:
        return reverse_lazy('user-home')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = 'Waiting'
        return super().form_valid(form)


class ListRequestView(views.ListView):
    queryset = Request.objects.all()
    template_name = 'requests/view-request.html'



# class UpdateRequestView(views.UpdateView):
#     queryset = Request.objects.all()
#     form_class = modelform_factory(Request, exclude=('status', 'user'))
#     template_name = 'requests/update-request.html'
#     success_url = reverse_lazy('user-home')

#     def form_valid(self, form):
#         form.instance.status = 'Waiting'
#         return super().form_valid(form)

class DeleteRequestView(views.DeleteView):
    queryset = Request.objects.all()
    template_name = 'requests/delete-request.html'
    success_url = reverse_lazy('user-home')

class ListNotificationView(views.ListView):
    queryset = RequestNotification.objects.all()
    template_name = 'requests/view-notifications.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        read_notifications = UserNotification.objects.filter(user=self.request.user, is_read=True)
        unread_notifications = UserNotification.objects.filter(user=self.request.user, is_read=False)
        context['read_notifications'] = read_notifications
        context['unread_notifications'] = unread_notifications
        return context