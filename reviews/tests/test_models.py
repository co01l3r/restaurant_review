from django.test import TestCase
from reviews.models import Restaurant


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
        