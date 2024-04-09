import json
from django.http import HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import get_user_model
from django.forms.models import modelform_factory

from TechSupportSystem.requests.models import Request
from TechSupportSystem.accounts.forms import EditProfileForm
from TechSupportSystem.departments.models import Department

from TechSupportSystem.helpers.mixins import (
    GetNotificationsMixin, VisibleToSuperUserMixin, VisibleToStaffMixin)
from TechSupportSystem.helpers.paginators import FlexiblePaginator

from django.core.paginator import EmptyPage, PageNotAnInteger


UserModel = get_user_model()



class ListRequestsView(GetNotificationsMixin, VisibleToStaffMixin, views.ListView):
    
    template_name = 'accounts/user-homepage.html'
    
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        per_page = self.request.GET.get('per_page', 10)  # Get user input page size
        paginator = FlexiblePaginator(self.get_queryset(), per_page)
        page_number = self.request.GET.get('page', 1)

        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)

        context['request_list'] = page.object_list
        context['paginator'] = paginator
        context['page_obj'] = page
        context['per_page'] = per_page
        
        return context
    
    
    def get_queryset(self):
        
        queryset = Request.objects.all().order_by('-created_at')
        if self.request.user.is_superuser:
            queryset = queryset
        else:
            queryset = queryset.filter(user__department=self.request.user.department)
            
        return queryset



class ListUsersView(GetNotificationsMixin, VisibleToStaffMixin, views.ListView):
    
    template_name = 'accounts/users.html'
    paginate_by = 10
    
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        context['current_user'] = self.request.user
        
        return context
    
    
    def get_queryset(self):
        
        queryset=UserModel.objects.all().order_by('username')
        if self.request.user.is_superuser:
            queryset = queryset
        elif self.request.user.is_staff:
            queryset = queryset.filter(department=self.request.user.department)
            
        return queryset



class EditUserView(GetNotificationsMixin, VisibleToSuperUserMixin, views.UpdateView):
    
    queryset = UserModel.objects.all()
    form_class = modelform_factory(UserModel, form=EditProfileForm, exclude=['password'])
    template_name = 'accounts/user-edit.html'
    
    
    def form_valid(self, form):
        
        was_manager = False
        if form.instance.profile.role == form.instance.department.management_role:
            was_manager = True
            
        user = form.save()
        user.profile.last_updated_by = self.request.user
        user.profile.save()
        
        if form.instance.profile.role == form.instance.department.management_role and not form.instance.department.manager:
            form.instance.department.manager = form.instance
            form.instance.department.save()
        if was_manager and form.instance.profile.role != form.instance.department.management_role:
            form.instance.department.manager = None
            form.instance.department.save()
            form.instance.is_staff = False
            form.instance.save()
            
        return HttpResponseRedirect(self.get_success_url())


    def get_success_url(self) -> str:
        
        return reverse_lazy('users')



class DeleteUserView(GetNotificationsMixin, VisibleToSuperUserMixin, views.DeleteView):
    
    queryset = UserModel.objects.all()
    template_name = 'accounts/user-delete.html'
    success_url = reverse_lazy('users')

class GetRolesForDepartmentView(views.View):
    
    # def get(self, request, *args, **kwargs):
        
    #     department_id = request.GET.get('department_id')
    #     department = Department.objects.get(pk=department_id)
    #     roles = department.roles.all()
    #     print({'roles': [{'id': role.id, 'name': role.title} for role in roles]})
        
    #     return JsonResponse({'roles': [{'id': role.id, 'name': role.title} for role in roles]})
    def post(self, request, *args, **kwargs):
        request_args = json.loads(request.body.decode('utf-8'))
        if request_args['HTTP_X_REQUESTED_WITH'] == 'XMLHttpRequest':  # Check if it's an AJAX request\
            department_id = request_args['department_id']
            print(department_id)
            department = Department.objects.get(pk=department_id)
            roles = department.roles.all()
            roles_data = [{'id': role.id, 'name': role.title} for role in roles]
            return JsonResponse({'roles': roles_data})
        else:
            print('Not AJAX')
            return JsonResponse({'error': 'Access denied'}, status=403)
        
    def get(self, request, *args, **kwargs):
        raise PermissionDenied()