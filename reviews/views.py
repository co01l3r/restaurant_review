from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import DatabaseError
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpRequest, HttpResponse
from typing import List, Union

from .forms import (LoginForm, RegistrationForm, RestaurantForm, ReviewForm,
                    VisitForm)
from .models import Restaurant, Review, Visit
from .utils import (calculate_user_total_spending_at_restaurant,
                    count_user_visits_to_restaurant)


# user
def register(request: HttpRequest) -> Union[render, redirect]:
    """
    Handle user registration.

    This function processes user registration. If the HTTP method is POST,
    it attempts to validate the registration form, create a new user,
    log in the user, and redirect to the home page upon success.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        Union[render, redirect]: An HTML response for rendering the registration form or
                a redirect to the home page if registration is successful.

    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        try:
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, 'Registration successful.')
                return redirect('home')
            else:
                messages.error(request, 'error')
        except Exception as e:
            messages.error(request, f'An error occurred during registration: {e}')
    else:
        form = RegistrationForm()

    return render(request, 'reviews/register.html', {'form': form})


def login_view(request):
    """
    Handle user login.

    This function processes user login. If the HTTP method is POST,
    it attempts to validate the login form, authenticate the user,
    and log in the user, redirecting to the restaurant list page upon success.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        Union[render, redirect]: An HTML response for rendering the login form or
                a redirect to the restaurant list page if login is successful.

    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful.')
                return redirect('restaurant_list')
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
        else:
            messages.error(request, 'error')
    else:
        form = LoginForm()

    return render(request, 'reviews/login.html', {'form': form})


# restaurant
@login_required
def add_restaurant(request: HttpRequest) -> Union[render, redirect]:
    """
    Add a new restaurant.

    This function handles the addition of a new restaurant. If the HTTP method is POST,
    it attempts to validate the restaurant form, save the new restaurant, and redirect
    to the restaurant list page upon success.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        Union[render, redirect]: An HTML response for rendering the restaurant form or
                a redirect to the restaurant list page if restaurant addition is successful.

    """
    if request.method == 'POST':
        form = RestaurantForm(request.POST)

        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.created_by = request.user
            restaurant.save()
            messages.success(request, 'Restaurant added successfully.')
            return redirect('restaurant_list')
        else:
            messages.error(request, 'error')
    else:
        form = RestaurantForm()

    return render(request, 'reviews/restaurant_form.html', {'form': form})


@login_required
def edit_restaurant(request: HttpRequest, restaurant_id: int) -> Union[render, redirect]:
    """
    Edit an existing restaurant.

    This function handles the editing of an existing restaurant. If the logged-in user
    is not the creator of the restaurant, a PermissionDenied exception is raised.
    If the HTTP method is POST, it attempts to validate the restaurant form, save the
    updated restaurant, and redirect to the restaurant list page upon success.

    Parameters:
        request (HttpRequest): The HTTP request object.
        restaurant_id (int): The ID of the restaurant to be edited.

    Returns:
        Union[render, redirect]: An HTML response for rendering the restaurant form or
                a redirect to the restaurant list page if restaurant editing is successful.

    Raises:
        PermissionDenied: If the logged-in user is not the creator of the restaurant.

    """
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.user != restaurant.created_by:
        raise PermissionDenied("You don't have permission to edit this restaurant.")

    if request.method == 'POST':
        form = RestaurantForm(request.POST, instance=restaurant)
        if form.is_valid():
            form.save()
            messages.success(request, 'Restaurant updated successfully.')
            return redirect('restaurant_list')
        else:
            messages.error(request, 'error')
    else:
        form = RestaurantForm(instance=restaurant)

    return render(request, 'reviews/restaurant_form.html', {'form': form, 'restaurant': restaurant})


@login_required
def delete_restaurant(request: HttpRequest, restaurant_id: int) -> Union[render, redirect]:
    """
    Delete an existing restaurant.

    This function handles the deletion of an existing restaurant. It checks if the logged-in
    user is the creator of the restaurant. If so, it attempts to delete the restaurant and
    redirects to the restaurant list page upon success. If the restaurant is not found or an
    error occurs during the deletion, appropriate error messages are displayed.

    Parameters:
        request (HttpRequest): The HTTP request object.
        restaurant_id (int): The ID of the restaurant to be deleted.

    Returns:
        Union[render, redirect]: A redirect to the restaurant list page if restaurant deletion is
                successful, or an HTML response for rendering the delete restaurant page.

    """
    try:
        restaurant = get_object_or_404(Restaurant, id=restaurant_id, created_by=request.user)
        restaurant_name = str(restaurant)

        if request.method == 'POST':
            restaurant.delete()
            messages.success(request, f'Restaurant "{restaurant_name}" deleted successfully.')
            return redirect('restaurant_list')

    except Restaurant.DoesNotExist:
        messages.error(request, f'Restaurant not found.')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')

    context = {'restaurant': restaurant}
    return render(request, 'reviews/delete_restaurant.html', context)


def restaurant_list(request: HttpRequest) -> Union[render]:
    """
    Display a list of restaurants.

    This function retrieves all restaurants from the database and renders the
    'restaurant_list.html' template with the list of restaurants. If an error
    occurs during the retrieval, an error message is displayed.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        Union[render]: An HTML response for rendering the restaurant list page.

    """
    try:
        restaurants = Restaurant.objects.all()
        return render(request, 'reviews/restaurant_list.html', {'restaurants': restaurants})

    except DatabaseError as e:
        messages.error(request, f'Error retrieving restaurant list: {str(e)}')
        return render(request, 'reviews/restaurant_list.html', {'restaurants': []})


def restaurant_detail(request: HttpRequest, restaurant_id: int) -> Union[render, HttpResponse]:
    """
    Display details for a specific restaurant.

    This function retrieves a specific restaurant from the database and calculates
    the user's visit count and total spending at that restaurant. It then renders
    the 'restaurant_detail.html' template with the restaurant details. If an error
    occurs during the retrieval or calculation, an error message is displayed, and
    the user is redirected to the restaurant list.

    Parameters:
        request (HttpRequest): The HTTP request object.
        restaurant_id (int): The ID of the restaurant to display.

    Returns:
        Union[render, HttpResponse]: An HTML response for rendering the restaurant
        details page or a redirect response to the restaurant list in case of an error.

    """
    try:
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        user = request.user

        visit_count = count_user_visits_to_restaurant(user, restaurant)
        total_spending = calculate_user_total_spending_at_restaurant(user, restaurant)

        context = {'restaurant': restaurant, 'visit_count': visit_count, 'total_spending': total_spending}
        return render(request, 'reviews/restaurant_detail.html', context)

    except Exception as e:
        messages.error(request, f'Error displaying restaurant details: {str(e)}')
        return redirect('restaurant_list')


# review
@login_required
def create_review(request: HttpRequest, restaurant_id: int) -> Union[render, redirect]:
    """
    Create or edit a review for a specific restaurant.

    This function handles the creation or editing of a review for a specific
    restaurant. If the user has already submitted a review for the restaurant,
    the existing review is retrieved and displayed in the form. If the user
    submits a new review or edits the existing one, the form is validated, and
    the review is saved. Success or error messages are displayed accordingly.

    Parameters:
        request (HttpRequest): The HTTP request object.
        restaurant_id (int): The ID of the restaurant for which the review is created.

    Returns:
        Union[render, redirect]: An HTML response for rendering the create review
        page or a redirect response to the restaurant detail page.

    """
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    user_review = Review.objects.filter(restaurant=restaurant, customer=request.user).first()

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=user_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.customer = request.user
            review.restaurant = restaurant
            review.save()

            messages.success(request, 'Review submitted successfully.')

            return redirect('restaurant_detail', restaurant_id=restaurant.id)
        else:
            messages.error(request, "error")
    else:
        form = ReviewForm(instance=user_review)

    context = {'restaurant': restaurant, 'form': form}
    return render(request, 'reviews/create_review.html', context)


@login_required
def user_reviews(request: HttpRequest) -> render:
    """
    Retrieve and display reviews submitted by the currently logged-in user.

    This function retrieves reviews submitted by the currently logged-in user
    and renders the 'user_reviews.html' template. If there is an error retrieving
    the reviews, an empty list is assigned, and an error message is displayed.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        render: An HTML response for rendering the 'user_reviews.html' template.

    """
    try:
        personal_reviews: List[Review] = Review.objects.filter(customer=request.user)
    except DatabaseError as e:
        personal_reviews = []
        messages.error(request, f"Error retrieving user reviews: {e}")

    return render(request, 'reviews/user_reviews.html', {'user_reviews': personal_reviews})


# visit
@login_required
def add_visit(request: HttpRequest, restaurant_id: int) -> render:
    """
    Add a visit to a restaurant for the currently logged-in user.

    This function handles the addition of a visit to a restaurant for the currently logged-in user.
    If the request method is POST and the form is valid, the visit is saved, and a success message is
    displayed. If there is an error in the form submission, an error message is displayed.

    Parameters:
        request (HttpRequest): The HTTP request object.
        restaurant_id (int): The ID of the restaurant to which the visit is being added.

    Returns:
        render: An HTML response for rendering the 'add_visit.html' template.

    """
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == 'POST':
        form = VisitForm(request.POST)
        if form.is_valid():
            visit = form.save(commit=False)
            visit.restaurant = restaurant
            visit.customer = request.user
            visit.save()
            messages.success(request, "Visit added successfully.")
            return redirect('restaurant_detail', restaurant_id=restaurant_id)
        else:
            messages.error(request, "error")
    else:
        form = VisitForm()

    return render(request, 'reviews/add_visit.html', {'form': form, 'restaurant': restaurant})


@login_required
def user_visits(request: HttpRequest) -> render:
    """
    Display the visits of the currently logged-in user.

    This function retrieves and displays the visits of the currently logged-in user,
    ordered by date in descending order.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        render: An HTML response for rendering the 'user_visits.html' template.

    """
    visits = Visit.objects.filter(customer=request.user).order_by('-date')
    return render(request, 'reviews/user_visits.html', {'user_visits': visits})


@login_required
def delete_visit(request: HttpRequest, visit_id: int) -> redirect:
    """
    Delete a visit for the currently logged-in user.

    This function deletes a visit for the currently logged-in user with the specified visit_id.

    Parameters:
        request (HttpRequest): The HTTP request object.
        visit_id (int): The ID of the visit to be deleted.

    Returns:
        redirect: A redirection to the 'user_visits' view after deleting the visit.

    """
    try:
        visit = get_object_or_404(Visit, id=visit_id, customer=request.user)
        visit_name = str(visit)
        visit.delete()
        messages.success(request, f'Visit "{visit_name}" deleted successfully.')
    except Visit.DoesNotExist:
        messages.error(request, f'Visit not found.')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')

    return redirect('user_visits')
