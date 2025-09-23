"""
Example test file for Django backend
This file demonstrates how to write and run tests in Django
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.management import call_command
import json


class BasicTestCase(TestCase):
    """
    Basic test case demonstrating Django testing fundamentals
    """
    
    def setUp(self):
        """
        Set up test data that will be available for all test methods
        This runs before each test method
        """
        self.client = Client()
        User = get_user_model()
        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_user_creation(self):
        """
        Test that a user can be created successfully
        """
        User = get_user_model()
        user = User.objects.create_user(
            username='newuser',
            email='new@example.com',
            password='newpass123'
        )
        
        # Assertions to verify the test
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.email, 'new@example.com')
        self.assertTrue(user.check_password('newpass123'))
        self.assertFalse(user.is_superuser)
    
    def test_user_authentication(self):
        """
        Test user authentication functionality
        """
        # Test login
        login_successful = self.client.login(
            username='testuser',
            password='testpass123'
        )
        self.assertTrue(login_successful)
        
        # Test logout
        self.client.logout()
        
        # Test failed login
        login_failed = self.client.login(
            username='testuser',
            password='wrongpassword'
        )
        self.assertFalse(login_failed)
    
    def test_admin_interface(self):
        """
        Test Django admin interface accessibility
        """
        # Test admin login page loads
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
        
        # Test admin login with credentials
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/admin/')
        # Should redirect or show admin interface
        self.assertIn(response.status_code, [200, 302])


class APITestCase(TestCase):
    """
    Test case for API endpoints (if you have any)
    """
    
    def setUp(self):
        self.client = Client()
        User = get_user_model()
        self.user = User.objects.create_user(
            username='apiuser',
            email='api@example.com',
            password='apipass123'
        )
    
    def test_api_response_format(self):
        """
        Test that API responses are in expected format
        """
        # Example test for a hypothetical API endpoint
        # Replace '/api/test/' with your actual API endpoint
        response = self.client.get('/api/test/')
        
        # If endpoint exists, test the response
        if response.status_code != 404:
            self.assertEqual(response.status_code, 200)
            # Test JSON response format
            try:
                data = json.loads(response.content)
                self.assertIsInstance(data, dict)
            except json.JSONDecodeError:
                # If not JSON, test HTML response
                self.assertIn('text/html', response.get('Content-Type', ''))


class DatabaseTestCase(TestCase):
    """
    Test case for database operations
    """
    
    def test_database_connection(self):
        """
        Test that database connection is working
        """
        # Try to create and retrieve a user
        User = get_user_model()
        user = User.objects.create_user(
            username='dbuser',
            email='db@example.com',
            password='dbpass123'
        )
        
        # Verify user was saved to database
        saved_user = get_user_model().objects.get(username='dbuser')
        self.assertEqual(saved_user.email, 'db@example.com')
        
        # Test database query
        user_count = get_user_model().objects.count()
        self.assertGreaterEqual(user_count, 1)
    
    def test_database_rollback(self):
        """
        Test that database changes are rolled back after each test
        """
        initial_count = get_user_model().objects.count()
        
        # Create a user in this test
        get_user_model().objects.create_user(
            username='rollbackuser',
            email='rollback@example.com',
            password='rollbackpass123'
        )
        
        # Verify user was created
        new_count = get_user_model().objects.count()
        self.assertEqual(new_count, initial_count + 1)
        
        # After this test ends, the user should be automatically deleted
        # This is Django's test isolation feature


class ManagementCommandTestCase(TestCase):
    """
    Test case for Django management commands
    """
    
    def test_management_commands(self):
        """
        Test that Django management commands work
        """
        # Test check command
        try:
            call_command('check')
        except SystemExit:
            # check command exits with code 1 if there are issues
            pass
        
        # Test migrate command (dry run)
        # Use showmigrations as a non-invasive check in tests
        try:
            call_command('showmigrations')
        except SystemExit:
            pass


class UtilityTestCase(TestCase):
    """
    Test case for utility functions and helper methods
    """
    
    def test_string_operations(self):
        """
        Test basic string operations
        """
        test_string = "Hello, World!"
        
        # Test string methods
        self.assertEqual(test_string.upper(), "HELLO, WORLD!")
        self.assertEqual(test_string.lower(), "hello, world!")
        self.assertTrue(test_string.startswith("Hello"))
        self.assertTrue(test_string.endswith("!"))
    
    def test_list_operations(self):
        """
        Test basic list operations
        """
        test_list = [1, 2, 3, 4, 5]
        
        # Test list methods
        self.assertEqual(len(test_list), 5)
        self.assertIn(3, test_list)
        self.assertEqual(sum(test_list), 15)
        self.assertEqual(max(test_list), 5)
        self.assertEqual(min(test_list), 1)
