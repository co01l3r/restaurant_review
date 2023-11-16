from django.contrib import messages
from .models import Visit
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect


def delete_object(request, model, object_id, template_name, success_url_name):
    try:
        obj = get_object_or_404(model, id=object_id)

        if request.method == 'POST':
            obj_name = str(obj)
            obj.delete()
            messages.success(request, f'{model.__name__} "{obj_name}" deleted successfully.')
            return redirect(success_url_name)

        context = {model.__name__.lower(): obj, 'success_url_name': success_url_name}
        return render(request, f'reviews/{template_name}', context)

    except Http404:
        messages.error(request, f'{model.__name__} not found.')
        return redirect(success_url_name)

    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
        return redirect(success_url_name)


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
