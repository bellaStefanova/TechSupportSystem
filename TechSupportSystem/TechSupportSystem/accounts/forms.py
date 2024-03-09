from django.contrib.auth import forms as auth_forms
from django.contrib.auth import get_user_model

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