from datetime import date

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

from reviews.models import Customer, Restaurant, Review, Visit


# customer
class CustomerModelTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword', email='test@example.com')

        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            cuisine='asian_cuisine',
            address='123 Test Street',
            created_by=self.user,
        )

        self.visit = Visit.objects.create(
            restaurant=self.restaurant,
            customer=self.user,
            date=date.today(),
            spending='25.50',
        )

        self.review = Review.objects.create(
            restaurant=self.restaurant,
            customer=self.user,
            rating=4,
            pricing='moderate',
            comment='Test comment',
        )

    def test_get_all_visits(self):
        customer = Customer.objects.get(username='testuser')

        all_visits = customer.get_all_visits()

        self.assertTrue(all(isinstance(visit, Visit) for visit in all_visits))

        self.assertIn(self.visit, all_visits)


# restaurant
class RestaurantModelTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword', email='test@example.com')

        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            cuisine='asian_cuisine',
            address='123 Test Street',
            created_by=self.user,
        )

        self.review1 = Review.objects.create(
            restaurant=self.restaurant,
            customer=self.user,
            rating=4,
            pricing='moderate',
            comment='Test comment 1',
        )

        self.user2 = get_user_model().objects.create_user(username='testuser2', password='testpassword2', email='test2@example.com')

        self.review2 = Review.objects.create(
            restaurant=self.restaurant,
            customer=self.user2,
            rating=5,
            pricing='high',
            comment='Test comment 2',
        )

    def test_average_rating(self):
        avg_rating = self.restaurant.average_rating()

        self.assertEqual(avg_rating, (4 + 5) / 2)

    def test_get_restaurant_pricing_category_eval(self):
        pricing_category_eval = self.restaurant.get_restaurant_pricing_category_eval()

        self.assertTrue(
            pricing_category_eval in ['high - moderate', 'moderate - high'],
            f"Unexpected pricing category evaluation: {pricing_category_eval}"
        )

    def test_get_restaurant_pricing_category_eval_no_reviews(self):
        restaurant_no_reviews = Restaurant.objects.create(
            name='Restaurant with No Reviews',
            cuisine='european_cuisine',
            address='456 Test Street',
            created_by=self.user,
        )

        pricing_category_eval = restaurant_no_reviews.get_restaurant_pricing_category_eval()

        self.assertIsNone(pricing_category_eval)


# review
class ReviewModelTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')

        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            cuisine='european_cuisine',
            address='Test Address',
            created_by=self.user
        )

    def test_unique_review_combination(self):
        review1 = Review.objects.create(
            restaurant=self.restaurant,
            customer=self.user,
            rating=4,
            pricing='moderate',
            comment='Test Comment 1'
        )

        with self.assertRaises(Exception) as context:
            Review.objects.create(
                restaurant=self.restaurant,
                customer=self.user,
                rating=5,
                pricing='high',
                comment='Test Comment 2'
            )

        self.assertIn('UNIQUE constraint failed', str(context.exception))

    def test_default_rating_value(self):
        review = Review.objects.create(
            restaurant=self.restaurant,
            customer=self.user,
            pricing='moderate',
            comment='Test Comment 3'
        )

        self.assertEqual(review.rating, 3)


# visit
class VisitModelTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='TestPassword123'
        )

        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            created_by=self.user
        )

    class VisitModelTestCase(TestCase):
        def setUp(self):
            self.user = get_user_model().objects.create_user(
                username='testuser',
                password='testpassword'
            )
            self.restaurant = Restaurant.objects.create(
                name='Test Restaurant',
                description='Test Description',
                created_by=self.user
            )

        def test_unique_visit_combination(self):
            visit1 = Visit.objects.create(
                restaurant=self.restaurant,
                customer=self.user,
                date=date(2023, 1, 1),
                spending=50.00
            )

            try:
                Visit.objects.create(
                    restaurant=self.restaurant,
                    customer=self.user,
                    date=date(2023, 1, 1),
                    spending=60.00
                )
            except IntegrityError:
                pass
            else:
                self.fail("IntegrityError not raised for non-unique visit combination")
