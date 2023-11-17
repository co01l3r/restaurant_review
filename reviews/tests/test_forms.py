from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from reviews.forms import RegistrationForm, LoginForm, RestaurantForm, ReviewForm, VisitForm
from reviews.models import Restaurant, Review, Visit
from django.urls import reverse
from datetime import date
from django import forms


# user
class RegistrationFormTest(TestCase):

    def test_registration_form_valid_data(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }

        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_registration_form_blank_data(self):
        form_data = {}

        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

    def test_registration_form_password_mismatch(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'mismatchedpassword',
        }

        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)


class LoginFormTest(TestCase):
    def test_login_form_valid_data(self):
        form_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        form = LoginForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_login_form_missing_data(self):
        form_data = {
            'username': '',
            'password': ''
        }
        form = LoginForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)


# restaurant
class RestaurantFormTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')

        self.client = Client()

    def test_restaurant_form_submission(self):
        self.client.login(username='testuser', password='testpassword')

        restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            cuisine='asian_cuisine',
            address='123 Test Street',
            created_by=self.user,
        )

        form_data = {
            'restaurant': restaurant.id,
            'customer': self.user.id,
            'rating': 4,
            'pricing': 'moderate',
            'comment': 'Test comment',
        }

        url = reverse('create_review', kwargs={'restaurant_id': restaurant.id})

        response = self.client.post(url, form_data)

        self.assertEqual(response.status_code, 302)

        self.assertEqual(Review.objects.count(), 1)

    def test_restaurant_form_validation(self):
        form = RestaurantForm(data={})

        self.assertFalse(form.is_valid())


# review
class ReviewFormTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')

        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            cuisine='asian_cuisine',
            address='123 Test Street',
            created_by=self.user,
        )

    def test_review_form_valid_data(self):
        form_data = {
            'rating': 4,
            'pricing': 'moderate',
            'comment': 'Test comment',
        }

        form = ReviewForm(data=form_data)

        self.assertTrue(form.is_valid())

        review = form.save(commit=False)
        review.restaurant = self.restaurant
        review.customer = self.user
        review.save()

        self.assertEqual(Review.objects.count(), 1)

    def test_review_form_invalid_data(self):
        form_data = {
            'rating': 6,
            'pricing': 'invalid_pricing',
            'comment': 'Test comment',
        }

        form = ReviewForm(data=form_data)

        self.assertFalse(form.is_valid())

        self.assertIn('rating', form.errors)
        self.assertIn('pricing', form.errors)

        self.assertEqual(Review.objects.count(), 0)


# visit
class VisitFormTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')

        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            cuisine='asian_cuisine',
            address='123 Test Street',
            created_by=self.user,
        )

    def test_visit_form_valid_data(self):
        form_data = {
            'date': date.today(),
            'spending': '25.50',
        }

        form = VisitForm(data=form_data)

        self.assertTrue(form.is_valid())

        visit = form.save(commit=False)
        visit.restaurant = self.restaurant
        visit.customer = self.user
        visit.save()

        self.assertEqual(Visit.objects.count(), 1)

    def test_visit_form_invalid_data(self):
        form_data = {
            'date': 'invalid_date',
            'spending': 'invalid_amount',
        }

        form = VisitForm(data=form_data)

        self.assertFalse(form.is_valid())

        self.assertIn('date', form.errors)
        self.assertIn('spending', form.errors)

        self.assertEqual(Visit.objects.count(), 0)
