from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model
from django.forms.models import modelform_factory
from .forms import RegisterForm, EditProfileForm
from TechSupportSystem.helpers.mixins import GetNotificationsMixin
from TechSupportSystem.requests.models import Request
from .models import Profile



UserModel = get_user_model()

class SignupView(views.CreateView):
    queryset = UserModel.objects.all()
    form_class = RegisterForm
    template_name = 'accounts/signup.html'

    def get_success_url(self) -> str:
        return reverse_lazy('signin')
    
class NextToFirstLoginView(views.CreateView):
    queryset = Profile.objects.all()
    form_class = modelform_factory(Profile, exclude=('user',))
    template_name = 'accounts/additional-details.html'
    
    def get_success_url(self) -> str:
        return reverse_lazy('user-home')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class SignInView(auth_views.LoginView):
    template_name = 'accounts/signin.html'
    redirect_authenticated_user = True

    def get_success_url(self) -> str:
        
        user = self.request.user
        # print(not user.profile)
        if user.is_authenticated:
            if not hasattr(user, 'profile') and not user.skip_initial_profile_details:
                return reverse_lazy('add-profile-details')
            return reverse_lazy('user-home')
            # print(hasattr(user, 'profile'))
            # try: 
            #     if user.profile:
            #         return reverse_lazy('user-home')
            # except RelatedObjectDoesNotExist:
            #     return reverse_lazy('add-profile-details')
    
    def form_valid(self, form):
        user = form.get_user()
        if user.skip_initial_profile_details == False:
            user.skip_initial_profile_details = True
            user.save()
        return super().form_valid(form)


        # return reverse_lazy('user-home')

class SignOutView(auth_views.LogoutView):
    next_page = reverse_lazy('signin')

class UserHomeView(GetNotificationsMixin, views.TemplateView):
    template_name = 'accounts/user-homepage.html'

    def get_context_data(self, **kwargs):
        all_requests = Request.objects.order_by('-created_at')
        context = super().get_context_data(**kwargs)
        # context['requests'] = self.request.user.request_set.all()
        # context['all_requests'] = Request.objects.all()
        context['all_requests'] = all_requests
        context['requests'] = all_requests.filter(user=self.request.user)
        return context
    
class ProfileDetailsView(GetNotificationsMixin, views.DetailView):
    queryset = UserModel.objects.all()
    template_name = 'accounts/profile-details.html'

    def get_object(self):
        return self.request.user
    

class ProfileEditView(GetNotificationsMixin, views.UpdateView):
    queryset = UserModel.objects.all()
    form_class = modelform_factory(UserModel, form=EditProfileForm, exclude=['password'])
    template_name = 'accounts/profile-edit.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self) -> str:
        return reverse_lazy('profile-details')
    
class ChangePasswordView(auth_views.PasswordChangeView):
    template_name = 'accounts/change-password.html'

    def get_success_url(self) -> str:
        return reverse_lazy('profile-details')