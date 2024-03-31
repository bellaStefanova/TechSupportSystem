from django.db.models.base import Model as Model
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import generic as views
from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model
from django.forms.models import modelform_factory
from django.views.decorators.cache import cache_control
from django.utils.decorators import method_decorator
from django.contrib import auth
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from TechSupportSystem.helpers.mixins import GetNotificationsMixin, VisibleToSuperUserMixin, VisibleToStaffMixin
from TechSupportSystem.requests.models import Request
from TechSupportSystem.departments.models import Department
from .models import Profile
from .forms import RegisterForm, EditProfileForm


UserModel = get_user_model()

'''Register view for new users - accessible for anonymous users only'''
class SignupView(views.CreateView):
    queryset = UserModel.objects.all()
    form_class = RegisterForm
    template_name = 'accounts/signup.html'

    def get_success_url(self) -> str:
        return reverse_lazy('signin')

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('user-home')
        return super().get(request, *args, **kwargs)

'''Sign in view for registered users - accessible for anonymous users only'''
class SignInView(auth_views.LoginView):
    template_name = 'accounts/signin.html'
    redirect_authenticated_user = True

    def get_success_url(self) -> str:
        user = self.request.user
        if user.is_authenticated:
            if not hasattr(user, 'profile') and not user.skip_initial_profile_details:
                return reverse_lazy('add-profile-details')
            if user.is_superuser:
                return reverse_lazy('dashboard')
            return reverse_lazy('user-home')


'''View for additional details for first time signed in users - accessible only once for authenticated users only,
once the url is loaded, it's not accessible anymore for the same user even if skipped. Details can be edited
in edit-profile view.'''
class NextToFirstLoginView(LoginRequiredMixin, views.CreateView):
    queryset = Profile.objects.all()
    form_class = modelform_factory(Profile, exclude=('user','last_updated_by'))
    template_name = 'accounts/additional-details.html'
    
    def get_success_url(self) -> str:
        return reverse_lazy('user-home')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.last_updated_by = self.request.user
        return super().form_valid(form)
    
    def get(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            return redirect('dashboard')
        if self.request.user.skip_initial_profile_details:
            return redirect('user-home')
        user = self.request.user
        user.skip_initial_profile_details = True
        user.save()
        return super().get(request, *args, **kwargs)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.request.user.department:
            department_roles = self.request.user.department.roles.all()
            manager = UserModel.objects.filter(department=self.request.user.department, profile__role=self.request.user.department.management_role).first()
            if manager:
                form.fields['role'].queryset = department_roles.exclude(pk=manager.profile.role.pk)
            else:
                form.fields['role'].queryset = department_roles
        return form


'''Sign out view - accessible for authenticated users only'''
@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name='dispatch')
class SignOutView(View):

    def get(self, request, *args, **kwargs):
        cookies = request.COOKIES
        auth.logout(request)
        return redirect(reverse('signin'))



'''User home view - accessible for authenticated users only
if the user is authenticated, the view will redirect to login and next home page'''
class UserHomeView(GetNotificationsMixin, views.TemplateView):
    template_name = 'accounts/user-homepage.html'

    def get_context_data(self, **kwargs):
        all_requests = Request.objects.order_by('-created_at')
        context = super().get_context_data(**kwargs)
        context['all_requests'] = all_requests
        context['request_list'] = all_requests.filter(user=self.request.user)
        return context
    
'''Profile details view - accessible for authenticated users only'''
class ProfileDetailsView(GetNotificationsMixin, views.DetailView):
    template_name = 'accounts/profile-details.html'

    def get_object(self):
        return self.request.user
    
'''Profile edit view - accessible for authenticated users only'''
class ProfileEditView(GetNotificationsMixin, views.UpdateView):
    queryset = UserModel.objects.all()
    form_class = modelform_factory(UserModel, form=EditProfileForm, exclude=('password', 'is_staff'))
    template_name = 'accounts/profile-edit.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self) -> str:
        return reverse_lazy('profile-details')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.request.user.department:
            department_roles = self.request.user.department.roles.all()
            manager = UserModel.objects.filter(department=self.request.user.department, profile__role=self.request.user.department.management_role).first()
            if manager:
                form.fields['role'].queryset = department_roles.exclude(pk=manager.profile.role.pk)
            else:
                form.fields['role'].queryset = department_roles
        return form

'''Change password view - accessible for authenticated users only'''
class ChangePasswordView(GetNotificationsMixin, auth_views.PasswordChangeView):
    template_name = 'accounts/change-password.html'

    def get_success_url(self) -> str:
        return reverse_lazy('profile-details')

