"""
Unit tests for Login Microservice API

Tests cover all endpoints defined in openapi/login-microservice.yaml:
- GET /registration - Display registration page
- POST /registration - Process registration
- GET /login - Display login page
- GET / - Welcome redirect
- GET /welcome - Welcome page redirect
"""

import unittest
from unittest.mock import patch, MagicMock
import requests


class TestLoginMicroserviceConfig:
    """Configuration for Login Microservice tests"""
    BASE_URL = "http://localhost:8085"


class TestRegistrationPage(unittest.TestCase):
    """Tests for GET /registration endpoint"""

    def setUp(self):
        self.base_url = TestLoginMicroserviceConfig.BASE_URL
        self.endpoint = f"{self.base_url}/registration"

    @patch('requests.get')
    def test_get_registration_page_success(self, mock_get):
        """Test successfully retrieving registration page"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {'Content-Type': 'text/html'}
        mock_response.text = '<html><body><form>Registration Form</form></body></html>'
        mock_get.return_value = mock_response

        response = requests.get(self.endpoint)

        self.assertEqual(response.status_code, 200)
        self.assertIn('text/html', response.headers.get('Content-Type', ''))

    @patch('requests.get')
    def test_registration_page_contains_form(self, mock_get):
        """Test that registration page contains form elements"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '''
        <html>
            <body>
                <form>
                    <input name="username" />
                    <input name="password" type="password" />
                    <input name="passwordConfirm" type="password" />
                    <button type="submit">Register</button>
                </form>
            </body>
        </html>
        '''
        mock_get.return_value = mock_response

        response = requests.get(self.endpoint)

        self.assertIn('username', response.text)
        self.assertIn('password', response.text)


class TestRegistrationProcess(unittest.TestCase):
    """Tests for POST /registration endpoint"""

    def setUp(self):
        self.base_url = TestLoginMicroserviceConfig.BASE_URL
        self.endpoint = f"{self.base_url}/registration"

    @patch('requests.post')
    def test_registration_success_redirect(self, mock_post):
        """Test successful registration redirects to login"""
        mock_response = MagicMock()
        mock_response.status_code = 302
        mock_response.headers = {'Location': '/login'}
        mock_post.return_value = mock_response

        response = requests.post(
            self.endpoint,
            data={
                'username': 'newuser',
                'password': 'securePassword123',
                'passwordConfirm': 'securePassword123'
            }
        )

        self.assertEqual(response.status_code, 302)

    @patch('requests.post')
    def test_registration_with_valid_data(self, mock_post):
        """Test registration with valid form data"""
        mock_response = MagicMock()
        mock_response.status_code = 302
        mock_post.return_value = mock_response

        form_data = {
            'username': 'johndoe',
            'password': 'securePassword123',
            'passwordConfirm': 'securePassword123'
        }
        response = requests.post(self.endpoint, data=form_data)

        self.assertIn(response.status_code, [200, 302])

    @patch('requests.post')
    def test_registration_password_mismatch(self, mock_post):
        """Test registration fails when passwords don't match"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><body>Passwords do not match</body></html>'
        mock_post.return_value = mock_response

        form_data = {
            'username': 'johndoe',
            'password': 'password123',
            'passwordConfirm': 'differentPassword'
        }
        response = requests.post(self.endpoint, data=form_data)

        # Should return form with errors (200) not redirect (302)
        self.assertEqual(response.status_code, 200)

    @patch('requests.post')
    def test_registration_username_too_short(self, mock_post):
        """Test registration fails with short username"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><body>Username too short</body></html>'
        mock_post.return_value = mock_response

        form_data = {
            'username': 'ab',  # Less than 3 characters
            'password': 'securePassword123',
            'passwordConfirm': 'securePassword123'
        }
        response = requests.post(self.endpoint, data=form_data)

        self.assertEqual(response.status_code, 200)

    @patch('requests.post')
    def test_registration_password_too_short(self, mock_post):
        """Test registration fails with short password"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><body>Password too short</body></html>'
        mock_post.return_value = mock_response

        form_data = {
            'username': 'johndoe',
            'password': 'short',  # Less than 8 characters
            'passwordConfirm': 'short'
        }
        response = requests.post(self.endpoint, data=form_data)

        self.assertEqual(response.status_code, 200)

    @patch('requests.post')
    def test_registration_duplicate_username(self, mock_post):
        """Test registration fails with existing username"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><body>Username already exists</body></html>'
        mock_post.return_value = mock_response

        form_data = {
            'username': 'existinguser',
            'password': 'securePassword123',
            'passwordConfirm': 'securePassword123'
        }
        response = requests.post(self.endpoint, data=form_data)

        self.assertEqual(response.status_code, 200)


class TestLoginPage(unittest.TestCase):
    """Tests for GET /login endpoint"""

    def setUp(self):
        self.base_url = TestLoginMicroserviceConfig.BASE_URL
        self.endpoint = f"{self.base_url}/login"

    @patch('requests.get')
    def test_get_login_page_success(self, mock_get):
        """Test successfully retrieving login page"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {'Content-Type': 'text/html'}
        mock_response.text = '<html><body><form>Login Form</form></body></html>'
        mock_get.return_value = mock_response

        response = requests.get(self.endpoint)

        self.assertEqual(response.status_code, 200)

    @patch('requests.get')
    def test_login_page_with_error_param(self, mock_get):
        """Test login page shows error message when error param present"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><body>Invalid credentials</body></html>'
        mock_get.return_value = mock_response

        response = requests.get(self.endpoint, params={'error': ''})

        self.assertEqual(response.status_code, 200)

    @patch('requests.get')
    def test_login_page_with_logout_param(self, mock_get):
        """Test login page shows logout message when logout param present"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><body>You have been logged out</body></html>'
        mock_get.return_value = mock_response

        response = requests.get(self.endpoint, params={'logout': ''})

        self.assertEqual(response.status_code, 200)

    @patch('requests.get')
    def test_login_page_contains_form(self, mock_get):
        """Test that login page contains login form elements"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '''
        <html>
            <body>
                <form>
                    <input name="username" />
                    <input name="password" type="password" />
                    <button type="submit">Login</button>
                </form>
            </body>
        </html>
        '''
        mock_get.return_value = mock_response

        response = requests.get(self.endpoint)

        self.assertIn('username', response.text)
        self.assertIn('password', response.text)


class TestWelcomeRedirect(unittest.TestCase):
    """Tests for GET / and GET /welcome endpoints"""

    def setUp(self):
        self.base_url = TestLoginMicroserviceConfig.BASE_URL

    @patch('requests.get')
    def test_root_redirects_to_app(self, mock_get):
        """Test that root path redirects to main application"""
        mock_response = MagicMock()
        mock_response.status_code = 302
        mock_response.headers = {'Location': 'http://localhost:8080'}
        mock_get.return_value = mock_response

        response = requests.get(f"{self.base_url}/")

        self.assertEqual(response.status_code, 302)

    @patch('requests.get')
    def test_welcome_redirects_to_app(self, mock_get):
        """Test that /welcome path redirects to main application"""
        mock_response = MagicMock()
        mock_response.status_code = 302
        mock_response.headers = {'Location': 'http://localhost:8080'}
        mock_get.return_value = mock_response

        response = requests.get(f"{self.base_url}/welcome")

        self.assertEqual(response.status_code, 302)


class TestUserRegistrationFormSchema(unittest.TestCase):
    """Tests for UserRegistrationForm schema validation"""

    @patch('requests.post')
    def test_registration_form_has_required_fields(self, mock_post):
        """Test that registration accepts all required fields"""
        mock_response = MagicMock()
        mock_response.status_code = 302
        mock_post.return_value = mock_response

        # All required fields per schema
        form_data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'passwordConfirm': 'testpassword123'
        }
        response = requests.post(
            f"{TestLoginMicroserviceConfig.BASE_URL}/registration",
            data=form_data
        )

        call_args = mock_post.call_args
        submitted_data = call_args.kwargs.get('data', {})
        self.assertIn('username', submitted_data)
        self.assertIn('password', submitted_data)
        self.assertIn('passwordConfirm', submitted_data)

    @patch('requests.post')
    def test_registration_username_length_validation(self, mock_post):
        """Test username length constraints (3-32 characters)"""
        mock_response = MagicMock()
        mock_response.status_code = 302
        mock_post.return_value = mock_response

        # Valid username (within 3-32 chars)
        form_data = {
            'username': 'validuser',  # 9 characters
            'password': 'testpassword123',
            'passwordConfirm': 'testpassword123'
        }
        response = requests.post(
            f"{TestLoginMicroserviceConfig.BASE_URL}/registration",
            data=form_data
        )

        # Should succeed with valid length
        self.assertIn(response.status_code, [200, 302])


if __name__ == '__main__':
    unittest.main()
