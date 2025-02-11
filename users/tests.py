"""
Tests for users app
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import User, UserSettings
from .forms import UserRegistrationForm, UserProfileForm, NotificationSettingsForm

class UserModelTests(TestCase):
    """Test cases for User model"""
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.instructor = User.objects.create_user(
            email='instructor@example.com',
            password='testpass123',
            first_name='Test',
            last_name='Instructor',
            is_instructor=True
        )

    def test_user_creation(self):
        """Test user creation"""
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpass123'))
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)

    def test_user_full_name(self):
        """Test get_full_name method"""
        self.assertEqual(self.user.get_full_name(), 'Test User')
        self.user.first_name = ''
        self.user.last_name = ''
        self.user.save()
        self.assertEqual(self.user.get_full_name(), 'test@example.com')

    def test_user_settings_creation(self):
        """Test UserSettings auto-creation"""
        settings = UserSettings.objects.get(user=self.user)
        self.assertTrue(settings.course_updates)
        self.assertFalse(settings.marketing_emails)

class UserFormTests(TestCase):
    """Test cases for User forms"""
    def test_registration_form_valid(self):
        """Test valid registration form"""
        form_data = {
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_registration_form_invalid(self):
        """Test invalid registration form"""
        form_data = {
            'email': 'invalid_email',
            'password1': 'testpass123',
            'password2': 'different',
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_profile_form_valid(self):
        """Test valid profile form"""
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        form_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'bio': 'Test bio'
        }
        form = UserProfileForm(data=form_data, instance=user)
        self.assertTrue(form.is_valid())

    def test_profile_form_avatar(self):
        """Test avatar upload in profile form"""
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        image = SimpleUploadedFile(
            "test.jpg",
            b"file_content",
            content_type="image/jpeg"
        )
        form_data = {
            'first_name': 'Test',
            'last_name': 'User'
        }
        form = UserProfileForm(
            data=form_data,
            files={'avatar': image},
            instance=user
        )
        self.assertTrue(form.is_valid())

class UserViewTests(TestCase):
    """Test cases for User views"""
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )

    def test_login_view(self):
        """Test login view"""
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

        # Test login with valid credentials
        response = self.client.post(reverse('users:login'), {
            'email': 'test@example.com',
            'password': 'testpass123'
        })
        self.assertRedirects(response, reverse('core:home'))

    def test_signup_view(self):
        """Test signup view"""
        response = self.client.get(reverse('users:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/signup.html')

        # Test signup with valid data
        response = self.client.post(reverse('users:signup'), {
            'email': 'new@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123',
            'first_name': 'New',
            'last_name': 'User'
        })
        self.assertRedirects(response, reverse('core:home'))
        self.assertTrue(User.objects.filter(email='new@example.com').exists())

    def test_settings_view(self):
        """Test settings view"""
        self.client.login(email='test@example.com', password='testpass123')
        
        response = self.client.get(reverse('users:settings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/settings.html')

        # Test updating notification settings
        response = self.client.post(
            reverse('users:update-notifications'),
            {'course_updates': False},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        settings = UserSettings.objects.get(user=self.user)
        self.assertFalse(settings.course_updates)

    def test_profile_view(self):
        """Test profile view"""
        self.client.login(email='test@example.com', password='testpass123')
        
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')

class InstructorViewTests(TestCase):
    """Test cases for instructor views"""
    def setUp(self):
        self.client = Client()
        self.instructor = User.objects.create_user(
            email='instructor@example.com',
            password='testpass123',
            first_name='Test',
            last_name='Instructor',
            is_instructor=True
        )
        self.client.login(email='instructor@example.com', password='testpass123')

    def test_instructor_dashboard(self):
        """Test instructor dashboard view"""
        response = self.client.get(reverse('users:instructor-dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/instructor/dashboard.html')

    def test_instructor_courses(self):
        """Test instructor courses view"""
        response = self.client.get(reverse('users:instructor-courses'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/instructor/courses.html')

    def test_instructor_earnings(self):
        """Test instructor earnings view"""
        response = self.client.get(reverse('users:instructor-earnings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/instructor/earnings.html')