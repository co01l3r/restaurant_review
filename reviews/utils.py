from decimal import Decimal
from reviews.models import Visit


def count_user_visits_to_restaurant(user, restaurant):
    user_visits = Visit.objects.filter(customer=user, restaurant=restaurant)
    return len(user_visits)


def calculate_user_total_spending_at_restaurant(user, restaurant):
    user_visits = Visit.objects.filter(customer=user, restaurant=restaurant)
    total_spending = sum(visit.spending for visit in user_visits)
    return total_spending
