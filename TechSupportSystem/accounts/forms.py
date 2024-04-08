from django.contrib.auth import forms as auth_forms
from django.contrib.auth import get_user_model
from .models import Profile
from django import forms

from TechSupportSystem.departments.models import Role

UserModel = get_user_model()

class RegisterForm(auth_forms.UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('username', 'email', 'department', 'password1', 'password2')
        help_texts = {
            'username': None,
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        self.fields['department'].required = True
        
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ('email', 'department', 'is_staff')
        
        
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    role = forms.ModelChoiceField(queryset=Role.objects.all(), required=False)

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].required = True
        
        if self.instance and self.instance.profile:
            self.fields['first_name'].initial = self.instance.profile.first_name
            self.fields['last_name'].initial = self.instance.profile.last_name
            self.fields['role'].initial = self.instance.profile.role
            if 'is_staff' in self.fields:
                self.fields['is_staff'].help_text = ''
            
    def save(self, commit=True):
        user = super(EditProfileForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if not user.is_superuser:
            user.department = self.cleaned_data['department']
        if commit:
            user.save()
        if user.profile:
            profile = user.profile
        else:
            profile = Profile(user=user)
        profile.first_name = self.cleaned_data['first_name']
        profile.last_name = self.cleaned_data['last_name']
        profile.role = self.cleaned_data['role']
        profile.save()
        return user