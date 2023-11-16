from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import DatabaseError
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (LoginForm, RegistrationForm, RestaurantForm, ReviewForm,
                    VisitForm)
from .models import Restaurant, Review, Visit
from .utils import (calculate_user_total_spending_at_restaurant,
                    count_user_visits_to_restaurant, delete_object)


# user
def register(request):
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
def add_restaurant(request):
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
def edit_restaurant(request, restaurant_id):
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
def delete_restaurant(request, restaurant_id):
    return delete_object(
        request,
        Restaurant,
        restaurant_id,
        'delete_restaurant_confirmation.html',
        'restaurant_list'
    )


def restaurant_list(request):
    try:
        restaurants = Restaurant.objects.all()
        return render(request, 'reviews/restaurant_list.html', {'restaurants': restaurants})

    except DatabaseError as e:
        messages.error(request, f'Error retrieving restaurant list: {str(e)}')
        return render(request, 'reviews/restaurant_list.html', {'restaurants': []})


def restaurant_detail(request, restaurant_id):
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
def create_review(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    user_review = Review.objects.filter(restaurant=restaurant, customer=request.user).first()

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=user_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.customer = request.user
            review.restaurant = restaurant
            review.save()
            return redirect('restaurant_detail', restaurant_id=restaurant.id)
        else:
            messages.error(request, "error")
    else:
        form = ReviewForm(instance=user_review)

    context = {'restaurant': restaurant, 'form': form}
    return render(request, 'reviews/create_review.html', context)


@login_required
def user_reviews(request):
    try:
        personal_reviews = Review.objects.filter(customer=request.user)
    except DatabaseError as e:
        personal_reviews = []
        messages.error(request, f"Error retrieving user reviews: {e}")

    return render(request, 'reviews/user_reviews.html', {'user_reviews': personal_reviews})


# visit
@login_required
def add_visit(request, restaurant_id):
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
def user_visits(request):
    visits = Visit.objects.filter(customer=request.user).order_by('-date')
    return render(request, 'reviews/user_visits.html', {'user_visits': visits})


@login_required
def delete_visit(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id)

    if visit.customer == request.user:
        visit.delete()

    return redirect('user_visits')
