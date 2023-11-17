from django.contrib import messages
from .models import Visit


def count_user_visits_to_restaurant(user, restaurant):
    try:
        user_visits = Visit.objects.filter(customer=user, restaurant=restaurant)
        visit_count = user_visits.count()
        return visit_count
    except Visit.DoesNotExist:
        messages.error("Error counting visits. Please try again.")
        return 0
    except Exception as e:
        messages.error("An unexpected error occurred. Please try again later.")
        return 0


def calculate_user_total_spending_at_restaurant(user, restaurant):
    try:
        user_visits = Visit.objects.filter(customer=user, restaurant=restaurant)
        total_spending = sum(visit.spending for visit in user_visits)
        return total_spending
    except Visit.DoesNotExist:
        messages.error("Error calculating total spending. Please try again.")
        return 0
    except AttributeError:
        messages.error("Error calculating total spending. Please check the data.")
        return 0
    except Exception as e:
        messages.error("An unexpected error occurred. Please try again later.")
        return 0
