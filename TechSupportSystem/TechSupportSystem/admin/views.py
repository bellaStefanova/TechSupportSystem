from django.db.models.query import QuerySet
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model
from django.forms.models import modelform_factory

from TechSupportSystem.departments.models import Department
from TechSupportSystem.requests.models import Request
from TechSupportSystem.accounts.forms import EditProfileForm


from TechSupportSystem.helpers.mixins import GetNotificationsMixin, VisibleToSuperUserMixin, VisibleToStaffMixin

UserModel = get_user_model()

class ListRequestsView(GetNotificationsMixin, VisibleToStaffMixin, views.ListView):
    template_name = 'accounts/user-homepage.html'
    
    def get_queryset(self):
        requests = Request.objects.all().order_by('-created_at')
        if self.request.user.is_superuser:
            return requests
        return requests.filter(user=self.request.user) #to make it department filtered
    

class ListUsersView(GetNotificationsMixin, VisibleToSuperUserMixin, views.ListView):
    queryset = UserModel.objects.all()
    template_name = 'accounts/users.html'


    
class EditUserView(GetNotificationsMixin, VisibleToSuperUserMixin, views.UpdateView):
    queryset = UserModel.objects.all()
    form_class = modelform_factory(UserModel, form=EditProfileForm, exclude=['password'])
    template_name = 'accounts/user-edit.html'

    def get_success_url(self) -> str:
        return reverse_lazy('users')
    
class DeleteUserView(GetNotificationsMixin, VisibleToSuperUserMixin, views.DeleteView):
    queryset = UserModel.objects.all()
    template_name = 'accounts/user-delete.html'
    success_url = reverse_lazy('users')
    
    # def get_object(self):
    #     return UserModel.objects.get
    
class StaffTeamView(GetNotificationsMixin, VisibleToStaffMixin, views.ListView):
    # queryset = UserModel.objects.all().filter()
    template_name = 'accounts/my-team.html'
    
    def get_queryset(self):
        departments = Department.objects.filter(manager=self.request.user)
        # queryset = UserModel.objects.all()
        return departments
