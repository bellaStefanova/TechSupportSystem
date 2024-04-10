from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Profile
from TechSupportSystem.requests.models import Request
from TechSupportSystem.departments.models import Department, Role

UserModel = get_user_model()

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserModel.objects.create_user(username='testuser', password='testpassword')

    def test_signup_view(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')

    def test_signin_view(self):
        response = self.client.get(reverse('signin'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signin.html')

    def test_signout_view(self):
        response = self.client.get(reverse('signout'))
        self.assertEqual(response.status_code, 302)

        self.client.force_login(self.user)
        response = self.client.get(reverse('signout'))
        self.assertEqual(response.status_code, 302)

    def test_user_home_view(self):
        response = self.client.get(reverse('user-home'))
        self.assertEqual(response.status_code, 302)

        self.client.force_login(self.user)
        response = self.client.get(reverse('user-home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/user-homepage.html')
    
    def test_signup_view_redirect_authenticated_user(self):
        self.client.force_login(self.user)
        
        response = self.client.get(reverse('signup'))
        
        self.assertRedirects(response, reverse('user-home'))