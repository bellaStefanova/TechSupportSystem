from django.forms.models import BaseModelForm
from django.shortcuts import render
from django.views import generic as views
from django.contrib.auth import get_user_model

from TechSupportSystem.notifications.models import RequestNotification
from TechSupportSystem.departments.models import Department
from .models import Request
from django.forms import modelform_factory
from django.urls import reverse_lazy
from TechSupportSystem.helpers.mixins import GetNotificationsMixin
from django.http import JsonResponse
from django.views import View
from django.db.models.signals import post_save
from .signals import edit_request_handler

UserModel = get_user_model()

class CreateRequestView(GetNotificationsMixin, views.CreateView):
    queryset = Request.objects.all()
    form_class = modelform_factory(Request, exclude=('status', 'user', 'worked_on_by', 'last_updated_by'))
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


class EditRequestView(views.UpdateView):
    queryset = Request.objects.all()
    template_name = 'requests/edit-request.html'
    
    def get_form_class(self) -> type[BaseModelForm]:
        if self.request.user.is_superuser:
            return modelform_factory(Request, exclude=('user', 'worked_on_by', 'last_updated_by'))
        return modelform_factory(Request, exclude=('status', 'user', 'worked_on_by', 'last_updated_by'))
    

    def form_valid(self, form):
        form.instance.last_updated_by = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse_lazy('view-request', kwargs={'pk': self.object.id})

class DeleteRequestView(GetNotificationsMixin, views.DeleteView):
    queryset = Request.objects.all()
    template_name = 'requests/delete-request.html'
    success_url = reverse_lazy('user-home')



class TakeRequestView(View):
    def post(self, request, request_id):
        support_request = Request.objects.get(id=request_id)
        support_request.status = 'Assigned'
        support_request.worked_on_by = request.user
        post_save.disconnect(edit_request_handler, sender=Request)
        support_request.save()
        post_save.connect(edit_request_handler, sender=Request)
        return JsonResponse({'message': 'Request taken'}, status=200)
    

class DashboardView(GetNotificationsMixin, views.TemplateView):
    
    template_name = 'requests/dashboard.html'
    
    def get_context_data(self, **kwargs):
        all_requests = Request.objects.all().order_by('-created_at')
        context = super().get_context_data(**kwargs)
        context['requests'] = all_requests
        context['all_requests_count'] = len(all_requests)
        context['waiting_requests_count'] = len(all_requests.filter(status='Waiting'))
        context['assigned_requests_count'] = len(all_requests.filter(status='Assigned'))
        context['resolved_requests_count'] = len(all_requests.filter(status='Resolved'))
        context['users'] = UserModel.objects.all()
        context['users_count'] = len(context['users'])
        context['departments_count'] = len(Department.objects.all())
        return context