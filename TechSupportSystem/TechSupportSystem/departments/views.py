from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic as views
from django.urls import reverse_lazy

from .models import Department

class DepartmentListView(views.ListView):
    template_name = 'departments/departments.html'
    queryset = Department.objects.all()
    

class DepartmentCreateView(views.CreateView):
    template_name = 'departments/create-department.html'
    model = Department
    fields = ('name', 'description', 'location', 'manager')
    success_url = reverse_lazy('departments')
    
    
class DepartmentEditView(views.UpdateView):
    template_name = 'departments/edit-department.html'
    model = Department
    fields = ('name', 'description', 'location', 'manager')
    success_url = reverse_lazy('departments')
    
    
class DepartmentDeleteView(views.DeleteView):
    template_name = 'departments/delete-department.html'
    model = Department
    success_url = reverse_lazy('departments')
