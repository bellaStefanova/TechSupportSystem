from django.db.models.base import Model as Model
from django.http import HttpResponseRedirect
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
from django.core.paginator import EmptyPage, PageNotAnInteger

from TechSupportSystem.helpers.mixins import GetNotificationsMixin
from TechSupportSystem.requests.models import Request
from TechSupportSystem.departments.models import Department, Role
from .models import Profile
from .forms import RegisterForm, EditProfileForm
from TechSupportSystem.helpers.paginators import FlexiblePaginator

UserModel = get_user_model()


'''Register view for new users - accessible for anonymous users only'''
class SignupView(views.CreateView):
    
    queryset = UserModel.objects.all()
    form_class = RegisterForm
    template_name = 'accounts/signup.html'


    def get_success_url(self) -> str:
        
        return reverse_lazy('signin')


    def get(self, request, *args, **kwargs):
        
        user = self.request.user
        
        if user.is_authenticated:
            if user.is_superuser:
                return redirect('dashboard')
            return redirect('user-home')
        return super().get(request, *args, **kwargs)


'''Sign in view for registered users - accessible for anonymous users only'''
class SignInView(auth_views.LoginView):
    
    template_name = 'accounts/signin.html'
    redirect_authenticated_user = True


    def get_success_url(self):
        
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
        
        instance = form.save(commit=False)
        profile = Profile.objects.get(user=self.request.user)
        profile.first_name = instance.first_name
        profile.last_name = instance.last_name
        profile.role = instance.role
        profile.last_updated_by = self.request.user
        profile.save()
        
        return HttpResponseRedirect(self.get_success_url())

    
    def get(self, request, *args, **kwargs):
        
        if self.request.user.is_superuser:
            return redirect('dashboard')
        
        if self.request.user.skip_initial_profile_details:
            return redirect('user-home')
        
        user = self.request.user
        user.skip_initial_profile_details = True
        user.save()
        profile = Profile(user=user)
        profile.save()
        
        return super().get(request, *args, **kwargs)
    
    
    def get_form(self, form_class=None):
        
        form = super().get_form(form_class)
        
        if self.request.user.department:
            department_roles = self.request.user.department.roles.all()
             
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
        queryset = queryset.filter(user=self.request.user)
        
        return queryset
    
    
'''Profile details view - accessible for authenticated users only'''
class ProfileDetailsView(GetNotificationsMixin, views.DetailView):
    
    template_name = 'accounts/profile-details.html'


    def get_object(self):
        
        return self.request.user
    
    
'''Profile edit view - accessible for authenticated users only'''
class ProfileEditView(GetNotificationsMixin, views.UpdateView):
    
    queryset = UserModel.objects.all()
    template_name = 'accounts/profile-edit.html'

    def get_object(self):
        
        return self.request.user


    def get_success_url(self):
        
        return reverse_lazy('profile-details')
    
    
    def get_form_class(self):
        
        if not self.request.user.is_superuser:
            return modelform_factory(UserModel, form=EditProfileForm, exclude=('password', 'is_staff'))
        
        return modelform_factory(UserModel, form=EditProfileForm, exclude=('password', 'is_staff', 'department', 'role'))
    
    
    def get_form(self, form_class=None):
        
        if self.request.user.is_superuser and not hasattr(self.request.user, 'profile'):
            
            profile = Profile(user=self.request.user)
            profile.save()
            
        form = super().get_form(form_class)
        
        if self.request.user.department:
            
            department_roles = self.request.user.department.roles.all()
            
            if self.request.user.department:
                existing_department_manager = Department.objects.filter(pk=self.request.user.department.pk, manager__isnull=False).first()
                    
            # form.fields['role'].queryset = department_roles
            form.fields['role'].queryset = Role.objects.all()
                
        return form
    
    
    def form_valid(self, form):
        
        was_manager = False
        
        if self.request.user.profile.role == self.request.user.department.management_role:
            was_manager = True
            
        self.object.profile.last_updated_by = self.request.user
        self.object = form.save()
        
        if form.instance.profile.role == self.request.user.department.management_role and not self.request.user.department.manager:
            self.request.user.department.manager = self.request.user
            self.request.user.department.save()
            
        if was_manager and form.instance.profile.role != self.request.user.department.management_role:
            self.request.user.department.manager = None
            self.request.user.department.save()
            self.request.user.is_staff = False
            self.request.user.save()
            
        return HttpResponseRedirect(self.get_success_url())
    
    
'''Change password view - accessible for authenticated users only'''
class ChangePasswordView(GetNotificationsMixin, auth_views.PasswordChangeView):
    
    template_name = 'accounts/change-password.html'


    def get_success_url(self) -> str:
        
        return reverse_lazy('profile-details')
