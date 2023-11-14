from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from reviews.forms import RegistrationForm, LoginForm


class FormsTestCase(TestCase):

    def test_registration_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'aSecurePassword123',
            'password2': 'aSecurePassword123',
        }

        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_login_form(self):
        user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
        )

        form_data = {
            'username': 'testuser',
            'password': 'password123',
        }

        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_login_form(self):
        user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
        )

        form_data = {
            'username': 'testuser',
            'password': 'incorrectpassword',
        }

        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_registration_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)