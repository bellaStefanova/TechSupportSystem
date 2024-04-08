from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import get_user_model
from django.forms.models import modelform_factory

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
        return requests.filter(user__department=self.request.user.department)
    

class ListUsersView(GetNotificationsMixin, VisibleToStaffMixin, views.ListView):
    model = UserModel
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
        print('Saving first time')
        user.profile.last_updated_by = self.request.user
        user.profile.save()
        print('Saving second time')
        # user.save()
        print(form.instance)
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
