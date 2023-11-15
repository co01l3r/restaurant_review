from typing import List, Tuple
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Avg
from collections import Counter


class Customer(AbstractUser):
    pass


class Restaurant(models.Model):

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

    def __str__(self):
        return self.name

    def average_rating(self):
        reviews = Review.objects.filter(restaurant=self)
        return reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    def get_most_used_pricing(self):
        pricing_counts = Counter(review.pricing for review in self.review_set.all())
        most_used_pricing, second_most_used_pricing = pricing_counts.most_common(2)

        # Function to determine sort key
        def sort_key(pricing):
            return (-pricing_counts[pricing], pricing)

        # Check if there's a tie
        if len(pricing_counts) > 1 and most_used_pricing[1] == second_most_used_pricing[1]:
            tied_pricing = [pricing for pricing, count in pricing_counts.items() if count == most_used_pricing[1]]

            # Specific tie scenarios
            if {'cheap', 'high'}.issubset(tied_pricing):
                return 'moderate'
            elif {'cheap', 'moderate'}.issubset(tied_pricing):
                return 'moderate'
            elif {'moderate', 'overpriced'}.issubset(tied_pricing):
                return 'high'

            # If none of the specific tie scenarios, return the most used pricing
            ordered_tied_pricing = sorted(tied_pricing, key=sort_key, reverse=True)
            return ' - '.join(ordered_tied_pricing)

        # If no tie, return the most used pricing
        return most_used_pricing[0]


class Review(models.Model):

    RATINGS_OPTIONS: List[Tuple[int, str]] = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    PRICING_CATEGORY_OPTION: List[Tuple[str, str]] = [
        ('cheap', 'Cheap'),
        ('moderate', 'Moderate'),
        ('high', 'High'),
        ('overpriced', 'Overpriced'),
    ]

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    customer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(max_length=1, choices=RATINGS_OPTIONS, default=3)
    pricing = models.CharField(max_length=30, choices=PRICING_CATEGORY_OPTION, default='moderate')
    comment = models.TextField(max_length=500, blank=True, null=True)

    class Meta:
        unique_together = ['restaurant', 'customer']

    def __str__(self):
        return f"{self.restaurant} - {self.customer.username} - {self.rating}"
