from django import forms
from django.forms.models import BaseModelForm
from django.shortcuts import render
from django.views import generic as views
from django.contrib.auth import get_user_model

from TechSupportSystem.notifications.models import RequestNotification
from TechSupportSystem.departments.models import Department
from .models import Request
from django.forms import modelform_factory, modelformset_factory
from django.urls import reverse_lazy
from TechSupportSystem.helpers.mixins import GetNotificationsMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import View
from django.db.models.signals import post_save
from .signals import edit_request_handler

UserModel = get_user_model()

class CreateRequestView(GetNotificationsMixin, views.CreateView):
    queryset = Request.objects.all()
    form_class = modelform_factory(Request, exclude=('status', 'user', 'worked_on_by', 'last_updated_by'),
                                   widgets={
                                       'urgency': forms.Select(attrs={'required': True})
                                   })
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
            return modelform_factory(Request, exclude=('user', 'worked_on_by', 'last_updated_by'),
                                     widgets={
                                     'urgency': forms.Select(attrs={'required': True})
                                 })
            
        return modelform_factory(Request, exclude=('status', 'user', 'worked_on_by', 'last_updated_by'),
                                 widgets={
                                     'title': forms.TextInput(attrs={'readonly': 'readonly'}),
                                     'urgency': forms.Select(attrs={'disabled': 'disabled', 'required': False})
                                 })
    

    def form_valid(self, form):
        form.instance.last_updated_by = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse_lazy('view-request', kwargs={'pk': self.object.id})

class CancelRequestView(GetNotificationsMixin, views.DeleteView):
    queryset = Request.objects.all()
    template_name = 'requests/cancel-request.html'
    
    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy('dashboard')
        return reverse_lazy('user-home')
    
    def form_valid(self, form):
        user = UserModel.objects.get(id=self.request.user.id)
        current_request = self.get_object()
        print(current_request)
        success_url = self.get_success_url()
        current_request.last_updated_by = user
        current_request.status = 'Cancelled'
        current_request.save()
        return HttpResponseRedirect(success_url)
    

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
    
    template_name = 'requests/dashboard2.html'
    
    def get_context_data(self, **kwargs):
        all_requests = Request.objects.all().order_by('-created_at')
        context = super().get_context_data(**kwargs)
        context['requests'] = all_requests
        context['last_requests'] = all_requests[:10]
        context['all_requests_count'] = len(all_requests)
        context['waiting_requests_count'] = len(all_requests.filter(status='Waiting'))
        context['assigned_requests_count'] = len(all_requests.filter(status='Assigned'))
        context['resolved_requests_count'] = len(all_requests.filter(status='Resolved'))
        context['low_urgency_requests_count'] = len(all_requests.filter(urgency='Low'))
        context['medium_urgency_requests_count'] = len(all_requests.filter(urgency='Medium'))
        context['high_urgency_requests_count'] = len(all_requests.filter(urgency='High'))
        context['critical_urgency_requests_count'] = len(all_requests.filter(urgency='Critical'))
        context['users'] = UserModel.objects.all()
        context['users_count'] = len(context['users'])
        context['departments_count'] = len(Department.objects.all())
        return context