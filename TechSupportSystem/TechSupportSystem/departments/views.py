from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic as views
from django.urls import reverse_lazy
from django.forms.models import modelform_factory

from TechSupportSystem.helpers.mixins import GetNotificationsMixin, VisibleToSuperUserMixin

from .models import Department, Role

class DepartmentListView(GetNotificationsMixin, VisibleToSuperUserMixin, views.ListView):
    template_name = 'departments/departments.html'
    queryset = Department.objects.all()
    

class DepartmentCreateView(GetNotificationsMixin, VisibleToSuperUserMixin, views.CreateView):
    template_name = 'departments/create-department.html'
    model = Department
    fields = ('name', 'description', 'location', 'manager')
    success_url = reverse_lazy('departments')
    
    
class DepartmentEditView(GetNotificationsMixin, VisibleToSuperUserMixin, views.UpdateView):
    template_name = 'departments/edit-department.html'
    model = Department
    fields = ('name', 'description', 'location', 'manager')
    success_url = reverse_lazy('departments')
    
    
class DepartmentDeleteView(GetNotificationsMixin, VisibleToSuperUserMixin, views.DeleteView):
    template_name = 'departments/delete-department.html'
    model = Department
    success_url = reverse_lazy('departments')

class RoleCreateView(GetNotificationsMixin, VisibleToSuperUserMixin, views.CreateView):
    template_name = 'departments/create-role.html'
    model = Department
    form_class = modelform_factory(Role, fields=('__all__'))
    success_url = reverse_lazy('roles')
    
class RoleListView(GetNotificationsMixin, VisibleToSuperUserMixin, views.ListView):
    template_name = 'departments/roles.html'
    queryset = Role.objects.all()
    
class RoleEditView(GetNotificationsMixin, VisibleToSuperUserMixin, views.UpdateView):
    template_name = 'departments/edit-role.html'
    model = Role
    form_class = modelform_factory(Role, fields=('__all__'))
    success_url = reverse_lazy('roles')
    
class RoleDeleteView(GetNotificationsMixin, VisibleToSuperUserMixin, views.DeleteView):
    template_name = 'departments/delete-role.html'
    model = Role
    success_url = reverse_lazy('roles')