from django.test import TestCase
from django.contrib.auth import get_user_model
from reviews.models import Restaurant, Review

# Restaurant
class RestaurantModelTest(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            cuisine='european_cuisine',
            address='123 Test Street, Test City'
        )

    def test_str_representation(self):
        self.assertEqual(str(self.restaurant), 'Test Restaurant')

    def test_default_cuisine(self):
        self.assertEqual(self.restaurant.cuisine, 'european_cuisine')

    def test_address_max_length(self):
        max_length = self.restaurant._meta.get_field('address').max_length
        self.assertLessEqual(len(self.restaurant.address), max_length)

    def test_create_and_retrieve(self):
        new_restaurant = Restaurant.objects.create(
            name='New Restaurant',
            cuisine='asian_cuisine',
            address='456 New Street, New City'
        )
        retrieved_restaurant = Restaurant.objects.get(name='New Restaurant')

        self.assertEqual(new_restaurant, retrieved_restaurant)


# Review
class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )

        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            cuisine='european_cuisine',
            address='123 Test Street, Test City'
        )

        self.review = Review.objects.create(
            restaurant=self.restaurant,
            customer=self.user,
            rating='4',
            pricing='moderate',
            comment='This is a test review.'
        )

    def test_str_representation(self):
        expected_str = f"{self.restaurant} - {self.user.username} - 4"
        self.assertEqual(str(self.review), expected_str)

    def test_default_values(self):
        self.assertEqual(self.review.rating, '4')
        self.assertEqual(self.review.pricing, 'moderate')
        self.assertEqual(self.review.comment, 'This is a test review.')