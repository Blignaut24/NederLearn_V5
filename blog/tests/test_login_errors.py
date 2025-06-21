"""
Test cases for login error message display functionality.

This module tests that invalid username/password combinations display
appropriate error messages on the login page.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class LoginErrorDisplayTest(TestCase):
    """Test cases for login error message display."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.login_url = reverse('account_login')
        
        # Create a test user
        User = get_user_model()
        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='correctpassword123'
        )
    
    def test_invalid_username_displays_error(self):
        """Test that invalid username displays error message."""
        response = self.client.post(self.login_url, {
            'login': 'invaliduser',
            'password': 'correctpassword123'
        })
        
        # Should not redirect (login failed)
        self.assertEqual(response.status_code, 200)
        
        # Should contain error message
        self.assertContains(response, 'my_errorlist')
        self.assertContains(response, 'username and/or password')
    
    def test_invalid_password_displays_error(self):
        """Test that invalid password displays error message."""
        response = self.client.post(self.login_url, {
            'login': 'testuser',
            'password': 'wrongpassword'
        })
        
        # Should not redirect (login failed)
        self.assertEqual(response.status_code, 200)
        
        # Should contain error message
        self.assertContains(response, 'my_errorlist')
        self.assertContains(response, 'username and/or password')
    
    def test_invalid_email_displays_error(self):
        """Test that invalid email displays error message."""
        response = self.client.post(self.login_url, {
            'login': 'wrong@example.com',
            'password': 'correctpassword123'
        })
        
        # Should not redirect (login failed)
        self.assertEqual(response.status_code, 200)
        
        # Should contain error message
        self.assertContains(response, 'my_errorlist')
        self.assertContains(response, 'email address and/or password')
    
    def test_both_invalid_displays_error(self):
        """Test that both invalid username and password display error message."""
        response = self.client.post(self.login_url, {
            'login': 'invaliduser',
            'password': 'wrongpassword'
        })
        
        # Should not redirect (login failed)
        self.assertEqual(response.status_code, 200)
        
        # Should contain error message
        self.assertContains(response, 'my_errorlist')
        self.assertContains(response, 'username and/or password')
    
    def test_valid_credentials_no_error(self):
        """Test that valid credentials don't display error message."""
        response = self.client.post(self.login_url, {
            'login': 'testuser',
            'password': 'correctpassword123'
        })
        
        # Should redirect (login successful)
        self.assertEqual(response.status_code, 302)
    
    def test_error_message_styling(self):
        """Test that error messages use correct CSS classes."""
        response = self.client.post(self.login_url, {
            'login': 'invaliduser',
            'password': 'wrongpassword'
        })
        
        # Should contain Bootstrap alert classes
        self.assertContains(response, 'alert alert-danger')
        
        # Should contain custom error list class
        self.assertContains(response, 'my_errorlist')
    
    def test_empty_form_submission(self):
        """Test that empty form submission displays appropriate errors."""
        response = self.client.post(self.login_url, {
            'login': '',
            'password': ''
        })
        
        # Should not redirect (form invalid)
        self.assertEqual(response.status_code, 200)
        
        # Should contain field-specific errors (not general form errors)
        # Empty fields typically generate field-specific errors, not form-level errors
        self.assertContains(response, 'text-danger')
