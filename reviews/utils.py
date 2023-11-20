from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Visit, Restaurant


def count_user_visits_to_restaurant(user: get_user_model(), restaurant: Restaurant) -> int:
    """
    Count the number of visits by a user to a specific restaurant.

    This function counts the number of visits by the specified user to the specified restaurant.

    Parameters:
        user (get_user_model): The user for whom visits are counted.
        restaurant (Restaurant): The restaurant for which visits are counted.

    Returns:
        int: The number of visits by the user to the restaurant.

    """
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


def calculate_user_total_spending_at_restaurant(user: get_user_model(), restaurant: Restaurant) -> float:
    """
    Calculate the total spending by a user at a specific restaurant.

    This function calculates the total spending by the specified user at the specified restaurant.

    Parameters:
        user (get_user_model): The user for whom total spending is calculated.
        restaurant (Restaurant): The restaurant for which total spending is calculated.

    Returns:
        float: The total spending by the user at the restaurant.

    """
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
