from django.shortcuts import render
from django.views import generic as views
from django.contrib.auth import get_user_model

from TechSupportSystem.notifications.models import RequestNotification
from .models import Request
from django.forms import modelform_factory
from django.urls import reverse_lazy
from TechSupportSystem.helpers.mixins import GetNotificationsMixin
from django.http import JsonResponse
from django.views import View

UserModel = get_user_model()

class CreateRequestView(GetNotificationsMixin, views.CreateView):
    queryset = Request.objects.all()
    form_class = modelform_factory(Request, exclude=('status', 'user', 'worked_on_by'))
    template_name = 'requests/create-request.html'

    def get_success_url(self) -> str:
        return reverse_lazy('user-home')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = 'Waiting'
       
        return super().form_valid(form)
    
    


class DetailsRequestView(GetNotificationsMixin, views.DetailView):
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

class DeleteRequestView(GetNotificationsMixin, views.DeleteView):
    queryset = Request.objects.all()
    template_name = 'requests/delete-request.html'
    success_url = reverse_lazy('user-home')



class TakeRequestView(View):
    def post(self, request, request_id):
        support_request = Request.objects.get(id=request_id)
        support_request.status = 'Assigned'
        support_request.worked_on_by = request.user
        support_request.save()
        return JsonResponse({'message': 'Request taken'}, status=200)