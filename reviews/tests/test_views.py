from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from reviews.forms import RegistrationForm
from django.contrib.messages import get_messages


# user
class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_view(self):
        test_user_data = {
            'username': 'testuser',
            'password1': 'TestPassword123',
            'password2': 'TestPassword123',
        }

        response = self.client.post(reverse('register'), data=test_user_data, follow=True)

        self.assertRedirects(response, reverse('home'))

        self.assertTrue(response.wsgi_request.user.is_authenticated)

        messages = list(response.context.get('messages', []))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Registration successful.')

    def test_register_view_invalid_data(self):
        invalid_user_data = {
            'username': '',
            'password1': '',
            'password2': '',
        }

        response = self.client.post(reverse('register'), data=invalid_user_data)

        self.assertEqual(response.status_code, 200)

        self.assertFalse(response.wsgi_request.user.is_authenticated)

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'error')


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_view(self):
        test_user = get_user_model().objects.create_user(username='testuser', password='TestPassword123')

        login_data = {
            'username': 'testuser',
            'password': 'TestPassword123',
        }

        response = self.client.post(reverse('login'), data=login_data)

        self.assertRedirects(response, reverse('restaurant_list'))

        self.assertTrue(response.wsgi_request.user.is_authenticated)

        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertEqual(messages, ['Login successful.'])

    def test_login_view_invalid_data(self):
        invalid_login_data = {
            'username': 'testuser',
            'password': 'WrongPassword',
        }
        response = self.client.post(reverse('login'), data=invalid_login_data)

        self.assertEqual(response.status_code, 200)

        self.assertFalse(response.wsgi_request.user.is_authenticated)

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Invalid username or password. Please try again.')

# restaurant
