from collections import Counter
from typing import List, Tuple

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Avg


# user
class Customer(AbstractUser):
    """
    Custom user model representing a customer.

    This model extends the Django AbstractUser model to include additional
    functionality related to customer-specific operations.

    Methods:
        get_all_visits() -> QuerySet:
            Get all visits associated with the customer, ordered by date.

    Attributes:
        Inherits attributes from the Django AbstractUser model.

    """
    def get_all_visits(self) -> models.QuerySet:
        """
        Get all visits associated with the customer, ordered by date.

        Returns:
            QuerySet: A queryset containing all visits associated with the customer,
                      ordered by date.

        Example:
            To get all visits for a customer, use:

            ```python
            customer = Customer.objects.get(username='example_user')
            all_visits = customer.get_all_visits()
            ```
        """
        return Visit.objects.filter(customer=self).order_by('date')


# restaurant
class Restaurant(models.Model):
    """
    Model representing a restaurant.

    This model stores information about a restaurant, including its name, cuisine,
    address, and the user who created it. It also includes methods for calculating
    the average rating and evaluating the pricing category.

    Attributes:
        name (str): The name of the restaurant.
        cuisine (str): The cuisine type of the restaurant.
        address (str): The address of the restaurant.
        created_by (User): The user who created the restaurant.

    Methods:
        __str__() -> str:
            Returns the string representation of the restaurant.

        average_rating() -> float:
            Calculates and returns the average rating of the restaurant.

        get_restaurant_pricing_category_eval() -> str or None:
            Evaluates and returns the pricing category of the restaurant.

    """
    RESTAURANT_TYPE_OPTIONS: List[Tuple[str, str]] = [
        ('african_cuisine', 'African cuisine'),
        ('american_cuisine', 'Cuisine of the Americas'),
        ('asian_cuisine', 'Asian cuisine'),
        ('european_cuisine', 'European cuisine'),
        ('oceanic_cuisine', 'Oceanic cuisine'),
    ]

    name = models.CharField(max_length=100)
    cuisine = models.CharField(max_length=50, choices=RESTAURANT_TYPE_OPTIONS, default='european_cuisine')
    address = models.TextField(max_length=200)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self) -> str:
        """
        Returns the string representation of the restaurant.

        Returns:
            str: The string representation of the restaurant.

        """
        return self.name

    def average_rating(self) -> float:
        """
        Calculates and returns the average rating of the restaurant.

        Returns:
            float: The average rating of the restaurant.

        """
        try:
            reviews = Review.objects.filter(restaurant=self)
            return reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        except Exception as e:
            return 0

    def get_restaurant_pricing_category_eval(self) -> str or None:
        """
        Evaluates and returns the pricing category of the restaurant.

        Returns:
            str or None: The pricing category of the restaurant or None if no pricing is available.

        """
        pricing_counts = Counter(review.pricing for review in self.review_set.all())

        # Check if pricing_counts is not empty
        if pricing_counts:
            most_used_pricing, *_ = pricing_counts.most_common(2)

            # Function to determine sort key
            def sort_key(pricing):
                return (-pricing_counts[pricing], pricing)

            # Check if there's a tie or only one pricing option
            if most_used_pricing and len(pricing_counts) > 1 and most_used_pricing[1] == \
                    pricing_counts.most_common(2)[1][1]:
                tied_pricing = [pricing for pricing, count in pricing_counts.items() if count == most_used_pricing[1]]

                # Specific tie scenarios
                tie_scenarios = [
                    (['cheap', 'high'], 'moderate'),
                    (['cheap', 'overpriced'], 'moderate'),
                    (['moderate', 'overpriced'], 'high')
                ]

                for pricings, result in tie_scenarios:
                    if set(pricings).issubset(tied_pricing):
                        return result

                # If none of the specific tie scenarios, return the most used pricing
                ordered_tied_pricing = sorted(tied_pricing, key=sort_key, reverse=True)
                return ' - '.join(ordered_tied_pricing)

            # If no tie or only one pricing option, return the most used pricing
            return most_used_pricing[0] if most_used_pricing else None

        # Return a default value if pricing_counts is empty
        return None


# review
class Review(models.Model):
    """
    Model representing a review.

    This model stores information about a review, including the associated
    restaurant, customer, creation timestamp, rating, pricing category, and
    optional comment.

    Attributes:
        restaurant (Restaurant): The restaurant being reviewed.
        customer (User): The user providing the review.
        created (DateTimeField): The timestamp when the review was created.
        rating (int): The rating given by the customer (1 to 5).
        pricing (str): The pricing category chosen by the customer.
        comment (str, optional): An optional comment provided by the customer.

    Meta:
        unique_together (list): Ensures uniqueness of reviews for a specific restaurant and customer.

    Methods:
        __str__() -> str:
            Returns the string representation of the review.

    """
    RATINGS_OPTIONS: List[Tuple[int, str]] = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    PRICING_CATEGORY_OPTIONS: List[Tuple[str, str]] = [
        ('cheap', 'Cheap'),
        ('moderate', 'Moderate'),
        ('high', 'High'),
        ('overpriced', 'Overpriced'),
    ]

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    customer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(choices=RATINGS_OPTIONS, default=3)
    pricing = models.CharField(max_length=30, choices=PRICING_CATEGORY_OPTIONS, default='moderate')
    comment = models.TextField(max_length=500, blank=True, null=True)

    class Meta:
        unique_together = ['restaurant', 'customer']

    def __str__(self) -> str:
        """
        Returns the string representation of the review.

        Returns:
            str: The string representation of the review.

        """
        return f"{self.customer.username} - {self.restaurant} - {self.rating}"


# visit
class Visit(models.Model):
    """
    Model representing a visit.

    This model stores information about a visit, including the associated
    restaurant, customer, visit date, and spending amount.

    Attributes:
        restaurant (Restaurant): The restaurant visited.
        customer (User): The user who made the visit.
        date (DateField): The date of the visit.
        spending (DecimalField): The amount spent during the visit.

    Meta:
        unique_together (list): Ensures uniqueness of visits for a specific restaurant, customer, and date.

    Methods:
        __str__() -> str:
            Returns the string representation of the visit.

    """
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date = models.DateField()
    spending = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ['restaurant', 'customer', 'date']

    def __str__(self) -> str:
        """
        Returns the string representation of the visit.

        Returns:
            str: The string representation of the visit.

        """
        return f"{self.customer.username} - {self.restaurant} - {self.date} - {self.spending}"
