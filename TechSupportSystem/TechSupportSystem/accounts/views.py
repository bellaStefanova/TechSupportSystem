from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model
from django.forms.models import modelform_factory

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
class NextToFirstLoginView(views.CreateView):
    queryset = Profile.objects.all()
    form_class = modelform_factory(Profile, exclude=('user',))
    template_name = 'accounts/additional-details.html'
    
    def get_success_url(self) -> str:
        return reverse_lazy('user-home')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get(self, request, *args, **kwargs):
        if self.request.user.skip_initial_profile_details:
            return redirect('user-home')
        user = self.request.user
        user.skip_initial_profile_details = True
        user.save()
        return super().get(request, *args, **kwargs)

'''Sign out view - accessible for authenticated users only'''
class SignOutView(auth_views.LogoutView):
    next_page = reverse_lazy('signin')


'''User home view - accessible for authenticated users only
if the user is authenticated, the view will redirect to login and next home page'''
class UserHomeView(GetNotificationsMixin, views.TemplateView):
    template_name = 'accounts/user-homepage.html'
    # login_url = reverse_lazy('signin')

    def get_context_data(self, **kwargs):
        all_requests = Request.objects.order_by('-created_at')
        context = super().get_context_data(**kwargs)
        context['all_requests'] = all_requests
        context['requests'] = all_requests.filter(user=self.request.user)
        return context
    
'''Profile details view - accessible for authenticated users only'''
class ProfileDetailsView(GetNotificationsMixin, views.DetailView):
    template_name = 'accounts/profile-details.html'
    # login_url = reverse_lazy('signin')

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

'''Change password view - accessible for authenticated users only'''
class ChangePasswordView(GetNotificationsMixin, auth_views.PasswordChangeView):
    template_name = 'accounts/change-password.html'

    def get_success_url(self) -> str:
        return reverse_lazy('profile-details')

