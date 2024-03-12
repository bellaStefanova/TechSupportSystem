from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model
from django.forms.models import modelform_factory
from .forms import RegisterForm

UserModel = get_user_model()

class SignupView(views.CreateView):
    queryset = UserModel.objects.all()
    form_class = RegisterForm
    template_name = 'accounts/signup.html'

class SignInView(auth_views.LoginView):
    template_name = 'accounts/signin.html'
    redirect_authenticated_user = True

    def get_success_url(self) -> str:

        if self.request.user.is_superuser:
            return reverse_lazy('dashboard')
        # return super().get_success_url()
        return reverse_lazy('user-home')

def test(request):
    return ('testing only')

class SignOutView(auth_views.LogoutView):
    next_page = reverse_lazy('signin')

class UserHomeView(views.TemplateView):
    template_name = 'accounts/user-homepage.html'