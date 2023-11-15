from typing import List, Tuple
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Avg


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
