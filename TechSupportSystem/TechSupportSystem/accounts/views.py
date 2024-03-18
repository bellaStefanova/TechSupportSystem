from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model
from django.forms.models import modelform_factory
from .forms import RegisterForm
from TechSupportSystem.helpers.mixins import GetNotificationsMixin
from TechSupportSystem.requests.models import Request

UserModel = get_user_model()

class SignupView(views.CreateView):
    queryset = UserModel.objects.all()
    form_class = RegisterForm
    template_name = 'accounts/signup.html'

    def get_success_url(self) -> str:
        return reverse_lazy('signin')

class SignInView(auth_views.LoginView):
    template_name = 'accounts/signin.html'
    redirect_authenticated_user = True

    def get_success_url(self) -> str:

        # if self.request.user.is_superuser:
        #     return reverse_lazy('dashboard')
        # return super().get_success_url()
        return reverse_lazy('user-home')

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