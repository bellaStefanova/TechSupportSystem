from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from .models import Request

UserModel = get_user_model()

class CreateRequestViewTests(TestCase):
    
    def test_create_request_view_authenticated_user(self):
        """
        Test that authenticated users can access the create request view.
        """
        self.client.force_login(UserModel.objects.create_user(username='test_user', password='test_password'))
        response = self.client.get(reverse('create-request'))
        self.assertEqual(response.status_code, 200)
        

class EditRequestViewTests(TestCase):
    
    def test_edit_request_view_authenticated_user(self):
        """
        Test that authenticated users can access the edit request view.
        """
        user = UserModel.objects.create_user(username='test_user', password='test_password')
        self.client.force_login(user)
        request = Request.objects.create(user=user, title='Test Request', description='Test Description')
        response = self.client.get(reverse('edit-request', kwargs={'pk': request.pk}))
        self.assertEqual(response.status_code, 200)
        
        
    def test_edit_request_view_superuser(self):
        """
        Test that superusers can access the edit request view.
        """
        superuser = UserModel.objects.create_superuser(username='superuser', email='superuser@example.com', password='test_password')
        self.client.force_login(superuser)
        request = Request.objects.create(title='Test Request', description='Test Description')
        response = self.client.get(reverse('edit-request', kwargs={'pk': request.pk}))
        self.assertEqual(response.status_code, 200)
        
    def test_edit_request_view_forbidden_status(self):
        """
        Test that edit request view returns a 404 error when trying to edit a request with a status other than 'Waiting' or 'Assigned'.
        """
        user = UserModel.objects.create_user(username='test_user', password='test_password')
        self.client.force_login(user)
        request = Request.objects.create(user=user, title='Test Request', description='Test Description', status='Resolved')
        response = self.client.get(reverse('edit-request', kwargs={'pk': request.pk}))
        self.assertEqual(response.status_code, 404)

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Request

UserModel = get_user_model()

class DashboardViewTests(TestCase):
    
    def test_dashboard_view_authenticated_user(self):
        """
        Test that authenticated users can access the dashboard view.
        """
        user = UserModel.objects.create_user(username='test_user', password='test_password')
        self.client.force_login(user)
        response = self.client.get(reverse('dashboard'))
        if user.is_superuser:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 403)
        
    def test_dashboard_view_anonymous_user(self):
        """
        Test that anonymous users are redirected to the login page when trying to access the dashboard view.
        """
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/signin/?next=/dashboard/')
