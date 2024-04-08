from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import get_user_model
from django.forms.models import modelform_factory

from TechSupportSystem.requests.models import Request
from TechSupportSystem.accounts.forms import EditProfileForm

from TechSupportSystem.helpers.mixins import GetNotificationsMixin, VisibleToSuperUserMixin, VisibleToStaffMixin
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage, PageNotAnInteger



class FlexiblePaginator(Paginator):
    
    def __init__(self, object_list, per_page, orphans=0, allow_empty_first_page=True):
        self.user_per_page = per_page
        super().__init__(object_list, per_page, orphans, allow_empty_first_page)


    def get_page(self, number):

        self.per_page = self.user_per_page
        return super().get_page(number)



UserModel = get_user_model()



class ListRequestsView(GetNotificationsMixin, VisibleToStaffMixin, views.ListView):
    
    template_name = 'accounts/user-homepage.html'
    paginate_by = 10
    
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        per_page = self.request.GET.get('per_page', self.paginate_by)  # Get user input page size
        paginator = FlexiblePaginator(self.get_queryset(), per_page)
        page_number = self.request.GET.get('page')

        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)

        context['your_objects'] = page
        context['paginator'] = paginator
        context['page_obj'] = page
        
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
