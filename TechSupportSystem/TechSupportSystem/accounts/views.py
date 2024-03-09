from django.shortcuts import render
from django.views import generic as views
from django.contrib.auth import get_user_model
from django.forms.models import modelform_factory
from .forms import RegisterForm

UserModel = get_user_model()

class SignupView(views.CreateView):
    queryset = UserModel.objects.all()
    form_class = RegisterForm
    # form_class = modelform_factory(UserModel, fields=('__all__'))
    template_name = 'accounts/signup.html'