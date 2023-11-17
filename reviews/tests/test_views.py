from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase, Client
from django.urls import reverse
from reviews.forms import RegistrationForm, RestaurantForm, ReviewForm, VisitForm
from reviews.models import Restaurant, Review, Visit


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
class RestaurantAddViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def test_add_restaurant_view(self):
        self.client.login(username='testuser', password='testpassword')

        form_data = {
            'name': 'Test Restaurant',
            'cuisine': 'european_cuisine',
            'address': 'Test Address',
        }

        response = self.client.post(reverse('add_restaurant'), data=form_data, follow=True)

        self.assertEqual(response.status_code, 200)

        new_restaurant = Restaurant.objects.first()
        self.assertEqual(new_restaurant.created_by, self.user)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Restaurant added successfully.')

        self.assertRedirects(response, reverse('restaurant_list'))

    def test_add_restaurant_view_invalid_form(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(reverse('add_restaurant'), data={}, follow=True)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'error')

        form = response.context['form']
        self.assertIsInstance(form, RestaurantForm)


class RestaurantEditViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            cuisine='european_cuisine',
            address='Test Address',
            created_by=self.user
        )

    def test_edit_restaurant_view(self):
        self.client.login(username='testuser', password='testpassword')

        form_data = {
            'name': 'Updated Restaurant',
            'cuisine': 'american_cuisine',
            'address': 'Updated Address',
        }

        response = self.client.post(reverse('edit_restaurant', args=[self.restaurant.id]), data=form_data)

        self.assertEqual(response.status_code, 302)  # 302 indicates a successful redirect
        updated_restaurant = Restaurant.objects.get(id=self.restaurant.id)
        self.assertEqual(updated_restaurant.name, 'Updated Restaurant')
        self.assertEqual(updated_restaurant.cuisine, 'american_cuisine')
        self.assertEqual(updated_restaurant.address, 'Updated Address')

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Restaurant updated successfully.')

        self.assertRedirects(response, reverse('restaurant_list'))

    def test_edit_restaurant_view_invalid_form(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(reverse('edit_restaurant', args=[self.restaurant.id]), data={})

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'error')

        form = response.context['form']
        self.assertIsInstance(form, RestaurantForm)


class RestaurantDeleteViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            cuisine='european_cuisine',
            address='Test Address',
            created_by=self.user
        )

    def test_delete_restaurant_view(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(reverse('delete_restaurant', args=[self.restaurant.id]))

        self.assertEqual(response.status_code, 302)  # 302 indicates a successful redirect
        self.assertFalse(Restaurant.objects.filter(id=self.restaurant.id).exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), f'Restaurant "{self.restaurant}" deleted successfully.')

        self.assertRedirects(response, reverse('restaurant_list'))


class RestaurantDetailViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            cuisine='european_cuisine',
            address='Test Address',
            created_by=self.user
        )

    def test_restaurant_detail_view(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('restaurant_detail', args=[self.restaurant.id]))

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['restaurant'], self.restaurant)

        self.assertEqual(response.context['visit_count'], 0)
        self.assertEqual(response.context['total_spending'], 0)

        self.assertTemplateUsed(response, 'reviews/restaurant_detail.html')


# review
class CreateReviewViewTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )

        # Create a test restaurant
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            cuisine='european_cuisine',
            address='Test Address',
            created_by=self.user
        )

    def test_create_review_view(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('create_review', args=[self.restaurant.id]))

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['restaurant'], self.restaurant)

        self.assertIsInstance(response.context['form'], ReviewForm)

        self.assertTemplateUsed(response, 'reviews/create_review.html')

    def test_create_review_view_post(self):
        self.client.login(username='testuser', password='testpassword')

        form_data = {
            'rating': 4,
            'pricing': 'moderate',
            'comment': 'Great experience!'
        }

        response = self.client.post(reverse('create_review', args=[self.restaurant.id]), data=form_data)

        self.assertRedirects(response, reverse('restaurant_detail', args=[self.restaurant.id]))

        review = Review.objects.get(restaurant=self.restaurant, customer=self.user)
        self.assertEqual(review.rating, form_data['rating'])
        self.assertEqual(review.pricing, form_data['pricing'])
        self.assertEqual(review.comment, form_data['comment'])

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Review submitted successfully.')

    def test_create_review_view_invalid_form(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(reverse('create_review', args=[self.restaurant.id]), data={})

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'error')

        form = response.context['form']
        self.assertIsInstance(form, ReviewForm)


# user reviews
class UserReviewsViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def test_user_reviews_view(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('user_reviews'))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'reviews/user_reviews.html')

        self.assertQuerysetEqual(response.context['user_reviews'], [])


# visit
class AddVisitViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            cuisine='european_cuisine',
            address='Test Address',
            created_by=self.user
        )

    def test_add_visit_view(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('add_visit', args=[self.restaurant.id]))

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['restaurant'], self.restaurant)

        self.assertIsInstance(response.context['form'], VisitForm)

        self.assertTemplateUsed(response, 'reviews/add_visit.html')

    def test_add_visit_view_post(self):
        self.client.login(username='testuser', password='testpassword')

        form_data = {
            'date': '2023-12-01',
            'spending': 50.00,
        }

        response = self.client.post(reverse('add_visit', args=[self.restaurant.id]), data=form_data)

        self.assertRedirects(response, reverse('restaurant_detail', args=[self.restaurant.id]))

        visit = Visit.objects.get(restaurant=self.restaurant, customer=self.user)
        self.assertEqual(str(visit.date), form_data['date'])
        self.assertEqual(visit.spending, form_data['spending'])

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Visit added successfully.')

    def test_add_visit_view_invalid_form(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(reverse('add_visit', args=[self.restaurant.id]), data={})

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'error')

        form = response.context['form']
        self.assertIsInstance(form, VisitForm)


# user visits
class UserVisitsViewTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def test_user_visits_view(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('user_visits'))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'reviews/user_visits.html')

        self.assertQuerysetEqual(response.context['user_visits'], [])

    def test_user_visits_view_with_visits(self):
        self.client.login(username='testuser', password='testpassword')

        Visit.objects.create(customer=self.user, date='2023-12-01', spending=50.00)
        Visit.objects.create(customer=self.user, date='2023-12-02', spending=40.00)

        response = self.client.get(reverse('user_visits'))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'reviews/user_visits.html')

        user_visits = response.context['user_visits']
        self.assertQuerysetEqual(user_visits, Visit.objects.filter(customer=self.user).order_by('-date'))

        for visit in user_visits:
            self.assertContains(response, visit.date.strftime('%b. %d, %Y').replace(" 0", " "))
            self.assertContains(response, str(visit.spending))


class DeleteVisitViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.visit = Visit.objects.create(
            customer=self.user,
            date='2023-12-01',
            spending=50.00
        )

    def test_delete_visit_view(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse('delete_visit', args=[self.visit.id]))

        self.assertEqual(response.status_code, 302)  # 302 indicates a successful redirect

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)

        self.assertRegex(str(messages[0]), r'Visit "testuser - None - 2023-12-01 - 50.\d+" deleted successfully.')

        self.assertRedirects(response, reverse('user_visits'))

        with self.assertRaises(Visit.DoesNotExist):
            Visit.objects.get(id=self.visit.id)
